import json
import warnings
from contextlib import contextmanager
from dataclasses import dataclass
import itertools
import os
import re
import time
from typing import (
    Any,
    Callable,
    ClassVar,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Sequence,
    Tuple,
)

from agate import Table

import dbt.exceptions
from dbt.adapters.base import Credentials
from dbt.adapters.base.query_headers import MacroQueryStringSetter
from dbt.adapters.databricks.__version__ import version as __version__
from dbt.clients import agate_helper
from dbt.contracts.connection import (
    AdapterResponse,
    Connection,
    ConnectionState,
    DEFAULT_QUERY_COMMENT,
)
from dbt.contracts.graph.manifest import Manifest
from dbt.events import AdapterLogger
from dbt.events.functions import fire_event
from dbt.events.types import ConnectionUsed, SQLQuery, SQLQueryStatus
from dbt.utils import DECIMALS

from dbt.adapters.spark.connections import SparkConnectionManager, _is_retryable_error

from databricks import sql as dbsql
from databricks.sql.client import (
    Connection as DatabricksSQLConnection,
    Cursor as DatabricksSQLCursor,
)
from databricks.sql.exc import Error as DBSQLError

logger = AdapterLogger("Databricks")

CATALOG_KEY_IN_SESSION_PROPERTIES = "databricks.catalog"
DBT_DATABRICKS_INVOCATION_ENV = "DBT_DATABRICKS_INVOCATION_ENV"
DBT_DATABRICKS_INVOCATION_ENV_REGEX = re.compile("^[A-z0-9\\-]+$")
DBT_DATABRICKS_HTTP_SESSION_HEADERS = "DBT_DATABRICKS_HTTP_SESSION_HEADERS"


@dataclass
class DatabricksCredentials(Credentials):
    host: str
    database: Optional[str]
    http_path: Optional[str] = None
    token: Optional[str] = None
    connect_retries: int = 0
    connect_timeout: int = 10
    session_properties: Optional[Dict[str, Any]] = None
    connection_parameters: Optional[Dict[str, Any]] = None
    retry_all: bool = False

    _ALIASES = {
        "catalog": "database",
    }

    @classmethod
    def __pre_deserialize__(cls, data: Dict[Any, Any]) -> Dict[Any, Any]:
        data = super().__pre_deserialize__(data)
        if "database" not in data:
            data["database"] = None
        return data

    def __post_init__(self) -> None:
        if "." in self.schema:
            logger.warning(
                f"The specified schema '{self.schema}' contains '.', "
                "which could cause unexpected behavior.\n"
                "It will not be allowed in the future release.\n"
                "If you are trying to set a catalog, please use `catalog` instead.\n"
            )

        session_properties = self.session_properties or {}
        if CATALOG_KEY_IN_SESSION_PROPERTIES in session_properties:
            if self.database is None:
                self.database = session_properties[CATALOG_KEY_IN_SESSION_PROPERTIES]
                del session_properties[CATALOG_KEY_IN_SESSION_PROPERTIES]
            else:
                raise dbt.exceptions.ValidationException(
                    f"Got duplicate keys: (`{CATALOG_KEY_IN_SESSION_PROPERTIES}` "
                    'in session_properties) all map to "database"'
                )
        self.session_properties = session_properties

        if self.database is not None:
            database = self.database.strip()
            if not database:
                raise dbt.exceptions.ValidationException(
                    f"Invalid catalog name : `{self.database}`."
                )
            self.database = database

        connection_parameters = self.connection_parameters or {}
        for key in (
            "server_hostname",
            "http_path",
            "access_token",
            "session_configuration",
            "catalog",
            "schema",
            "_user_agent_entry",
        ):
            if key in connection_parameters:
                raise dbt.exceptions.ValidationException(
                    f"The connection parameter `{key}` is reserved."
                )
        if "http_headers" in connection_parameters:
            http_headers = connection_parameters["http_headers"]
            if not isinstance(http_headers, dict) or any(
                not isinstance(key, str) or not isinstance(value, str)
                for key, value in http_headers.items()
            ):
                raise dbt.exceptions.ValidationException(
                    "The connection parameter `http_headers` should be dict of strings: "
                    f"{http_headers}."
                )
        self.connection_parameters = connection_parameters

    @property
    def type(self) -> str:
        return "databricks"

    @property
    def unique_field(self) -> str:
        return self.host

    def connection_info(self, *, with_aliases: bool = False) -> Iterable[Tuple[str, Any]]:
        as_dict = self.to_dict(omit_none=False)
        connection_keys = set(self._connection_keys(with_aliases=with_aliases))
        aliases: List[str] = []
        if with_aliases:
            aliases = [k for k, v in self._ALIASES.items() if v in connection_keys]
        for key in itertools.chain(self._connection_keys(with_aliases=with_aliases), aliases):
            if key in as_dict:
                yield key, as_dict[key]

    def _connection_keys(self, *, with_aliases: bool = False) -> Tuple[str, ...]:
        # Assuming `DatabricksCredentials.connection_info(self, *, with_aliases: bool = False)`
        # is called from only:
        #
        # - `Profile` with `with_aliases=True`
        # - `DebugTask` without `with_aliases` (`False` by default)
        #
        # Thus, if `with_aliases` is `True`, `DatabricksCredentials._connection_keys` should return
        # the internal key names; otherwise it can use aliases to show in `dbt debug`.
        connection_keys = ["host", "http_path", "schema"]
        if with_aliases:
            connection_keys.insert(2, "database")
        elif self.database:
            connection_keys.insert(2, "catalog")
        if self.session_properties:
            connection_keys.append("session_properties")
        return tuple(connection_keys)


class DatabricksSQLConnectionWrapper:
    """Wrap a Databricks SQL connector in a way that no-ops transactions"""

    _conn: DatabricksSQLConnection
    _cursors: List[DatabricksSQLCursor]

    def __init__(self, conn: DatabricksSQLConnection):
        self._conn = conn
        self._cursors = []

    def cursor(self) -> "DatabricksSQLCursorWrapper":
        cursor = self._conn.cursor()
        self._cursors.append(cursor)
        return DatabricksSQLCursorWrapper(cursor)

    def cancel(self) -> None:
        cursors: List[DatabricksSQLCursor] = self._cursors

        for cursor in cursors:
            try:
                cursor.cancel()
            except DBSQLError as exc:
                logger.debug("Exception while cancelling query: {}".format(exc))
                _log_dbsql_errors(exc)

    def close(self) -> None:
        try:
            self._conn.close()
        except DBSQLError as exc:
            logger.debug("Exception while closing connection: {}".format(exc))
            _log_dbsql_errors(exc)

    def rollback(self, *args: Any, **kwargs: Any) -> None:
        logger.debug("NotImplemented: rollback")


class DatabricksSQLCursorWrapper:
    """Wrap a Databricks SQL cursor in a way that no-ops transactions"""

    _cursor: DatabricksSQLCursor

    def __init__(self, cursor: DatabricksSQLCursor):
        self._cursor = cursor

    def cancel(self) -> None:
        try:
            self._cursor.cancel()
        except DBSQLError as exc:
            logger.debug("Exception while cancelling query: {}".format(exc))
            _log_dbsql_errors(exc)

    def close(self) -> None:
        try:
            self._cursor.close()
        except DBSQLError as exc:
            logger.debug("Exception while closing cursor: {}".format(exc))
            _log_dbsql_errors(exc)

    def fetchall(self) -> Sequence[Tuple]:
        return self._cursor.fetchall()

    def fetchone(self) -> Optional[Tuple]:
        return self._cursor.fetchone()

    def execute(self, sql: str, bindings: Optional[Sequence[Any]] = None) -> None:
        if sql.strip().endswith(";"):
            sql = sql.strip()[:-1]
        if bindings is not None:
            bindings = [self._fix_binding(binding) for binding in bindings]
        self._cursor.execute(sql, bindings)

    @classmethod
    def _fix_binding(cls, value: Any) -> Any:
        """Convert complex datatypes to primitives that can be loaded by
        the Spark driver"""
        if isinstance(value, DECIMALS):
            return float(value)
        else:
            return value

    @property
    def description(
        self,
    ) -> Sequence[
        Tuple[
            str,
            str,
            Optional[int],
            Optional[int],
            Optional[int],
            Optional[int],
            Optional[bool],
        ]
    ]:
        return self._cursor.description

    def schemas(self, catalog_name: str, schema_name: Optional[str] = None) -> None:
        self._cursor.schemas(catalog_name=catalog_name, schema_name=schema_name)

    def __del__(self) -> None:
        if self._cursor.open:
            # This should not happen. The cursor should explicitly be closed.
            self._cursor.close()
            with warnings.catch_warnings():
                warnings.simplefilter("always")
                warnings.warn("The cursor was closed by destructor.")


DATABRICKS_QUERY_COMMENT = f"""
{{%- set comment_dict = {{}} -%}}
{{%- do comment_dict.update(
    app='dbt',
    dbt_version=dbt_version,
    dbt_databricks_version='{__version__}',
    databricks_sql_connector_version='{dbsql.__version__}',
    profile_name=target.get('profile_name'),
    target_name=target.get('target_name'),
) -%}}
{{%- if node is not none -%}}
  {{%- do comment_dict.update(
    node_id=node.unique_id,
  ) -%}}
{{% else %}}
  {{# in the node context, the connection name is the node_id #}}
  {{%- do comment_dict.update(connection_name=connection_name) -%}}
{{%- endif -%}}
{{{{ return(tojson(comment_dict)) }}}}
"""


class DatabricksMacroQueryStringSetter(MacroQueryStringSetter):
    def _get_comment_macro(self) -> Optional[str]:
        if self.config.query_comment.comment == DEFAULT_QUERY_COMMENT:
            return DATABRICKS_QUERY_COMMENT
        else:
            return self.config.query_comment.comment


class DatabricksConnectionManager(SparkConnectionManager):
    TYPE: ClassVar[str] = "databricks"

    def set_query_header(self, manifest: Manifest) -> None:
        self.query_header = DatabricksMacroQueryStringSetter(self.profile, manifest)

    @contextmanager
    def exception_handler(self, sql: str) -> Iterator[None]:
        try:
            yield

        except DBSQLError as exc:
            logger.debug(f"Error while running:\n{sql}")
            _log_dbsql_errors(exc)
            raise dbt.exceptions.RuntimeException(str(exc)) from exc

        except Exception as exc:
            logger.debug(f"Error while running:\n{sql}")
            logger.debug(exc)
            if len(exc.args) == 0:
                raise

            thrift_resp = exc.args[0]
            if hasattr(thrift_resp, "status"):
                msg = thrift_resp.status.errorMessage
                raise dbt.exceptions.RuntimeException(msg) from exc
            else:
                raise dbt.exceptions.RuntimeException(str(exc)) from exc

    def add_query(
        self,
        sql: str,
        auto_begin: bool = True,
        bindings: Optional[Any] = None,
        abridge_sql_log: bool = False,
        *,
        close_cursor: bool = False,
    ) -> Tuple[Connection, Any]:
        conn, cursor = super().add_query(sql, auto_begin, bindings, abridge_sql_log)
        if close_cursor and hasattr(cursor, "close"):
            cursor.close()
        return conn, cursor

    def execute(
        self, sql: str, auto_begin: bool = False, fetch: bool = False
    ) -> Tuple[AdapterResponse, Table]:
        sql = self._add_query_comment(sql)
        _, cursor = self.add_query(sql, auto_begin)
        try:
            response = self.get_response(cursor)
            if fetch:
                table = self.get_result_from_cursor(cursor)
            else:
                table = agate_helper.empty_table()
            return response, table
        finally:
            cursor.close()

    def _execute_cursor(
        self, log_sql: str, f: Callable[[DatabricksSQLCursorWrapper], None]
    ) -> Table:
        connection = self.get_thread_connection()

        fire_event(ConnectionUsed(conn_type=self.TYPE, conn_name=connection.name))

        cursor: Optional[DatabricksSQLCursorWrapper] = None
        try:
            with self.exception_handler(log_sql):
                fire_event(SQLQuery(conn_name=connection.name, sql=log_sql))
                pre = time.time()

                handle: DatabricksSQLConnectionWrapper = connection.handle
                cursor = handle.cursor()
                f(cursor)

                fire_event(
                    SQLQueryStatus(
                        status=str(self.get_response(cursor)), elapsed=round((time.time() - pre), 2)
                    )
                )

            return self.get_result_from_cursor(cursor)
        finally:
            if cursor is not None:
                cursor.close()

    def list_schemas(self, database: str, schema: Optional[str] = None) -> Table:
        return self._execute_cursor(
            f"GetSchemas(database={database}, schema={schema})",
            lambda cursor: cursor.schemas(catalog_name=database, schema_name=schema),
        )

    @classmethod
    def validate_creds(cls, creds: DatabricksCredentials, required: List[str]) -> None:
        for key in required:
            if not hasattr(creds, key):
                raise dbt.exceptions.DbtProfileError(
                    "The config '{}' is required to connect to Databricks".format(key)
                )

    @classmethod
    def validate_invocation_env(cls, invocation_env: str) -> None:
        # Thrift doesn't allow nested () so we need to ensure that the passed user agent is valid
        if not DBT_DATABRICKS_INVOCATION_ENV_REGEX.search(invocation_env):
            raise dbt.exceptions.ValidationException(
                f"Invalid invocation environment: {invocation_env}"
            )

    @classmethod
    def get_all_http_headers(
        cls, user_http_session_headers: Dict[str, str]
    ) -> List[Tuple[str, str]]:
        http_session_headers_str: Optional[str] = os.environ.get(
            DBT_DATABRICKS_HTTP_SESSION_HEADERS
        )

        http_session_headers_dict: Dict[str, str] = (
            {
                k: v if isinstance(v, str) else json.dumps(v)
                for k, v in json.loads(http_session_headers_str).items()
            }
            if http_session_headers_str is not None
            else {}
        )

        intersect_http_header_keys = (
            user_http_session_headers.keys() & http_session_headers_dict.keys()
        )

        if len(intersect_http_header_keys) > 0:
            raise dbt.exceptions.ValidationException(
                f"Intersection with reserved http_headers in keys: {intersect_http_header_keys}"
            )

        http_session_headers_dict.update(user_http_session_headers)

        return list(http_session_headers_dict.items())

    @classmethod
    def open(cls, connection: Connection) -> Connection:
        if connection.state == ConnectionState.OPEN:
            logger.debug("Connection is already open, skipping open.")
            return connection

        creds: DatabricksCredentials = connection.credentials
        exc: Optional[Exception] = None

        user_agent_entry = f"dbt-databricks/{__version__}"

        invocation_env = os.environ.get(DBT_DATABRICKS_INVOCATION_ENV)
        if invocation_env is not None and len(invocation_env) > 0:
            cls.validate_invocation_env(invocation_env)
            user_agent_entry = f"{user_agent_entry}; {invocation_env}"

        if creds.http_path is None:
            raise dbt.exceptions.DbtProfileError(
                "`http_path` must set when" " using the dbsql method to connect to Databricks"
            )
        required_fields = ["host", "http_path", "token"]

        cls.validate_creds(creds, required_fields)

        connection_parameters = creds.connection_parameters.copy()  # type: ignore[union-attr]

        http_headers: List[Tuple[str, str]] = cls.get_all_http_headers(
            connection_parameters.pop("http_headers", {})
        )

        for i in range(1 + creds.connect_retries):
            try:
                # TODO: what is the error when a user specifies a catalog they don't have access to
                conn: DatabricksSQLConnection = dbsql.connect(
                    server_hostname=creds.host,
                    http_path=creds.http_path,
                    access_token=creds.token,
                    http_headers=http_headers if http_headers else None,
                    session_configuration=creds.session_properties,
                    catalog=creds.database,
                    # schema=creds.schema,  # TODO: Explicitly set once DBR 7.3LTS is EOL.
                    _user_agent_entry=user_agent_entry,
                    **connection_parameters,
                )
                handle = DatabricksSQLConnectionWrapper(conn)
                break
            except Exception as e:
                exc = e
                if isinstance(e, EOFError):
                    # The user almost certainly has invalid credentials.
                    # Perhaps a token expired, or something
                    msg = "Failed to connect"
                    if creds.token is not None:
                        msg += ", is your token valid?"
                    raise dbt.exceptions.FailedToConnectException(msg) from e
                retryable_message = _is_retryable_error(e)
                if retryable_message and creds.connect_retries > 0:
                    msg = (
                        f"Warning: {retryable_message}\n\tRetrying in "
                        f"{creds.connect_timeout} seconds "
                        f"({i} of {creds.connect_retries})"
                    )
                    logger.warning(msg)
                    time.sleep(creds.connect_timeout)
                elif creds.retry_all and creds.connect_retries > 0:
                    msg = (
                        f"Warning: {getattr(exc, 'message', 'No message')}, "
                        f"retrying due to 'retry_all' configuration "
                        f"set to true.\n\tRetrying in "
                        f"{creds.connect_timeout} seconds "
                        f"({i} of {creds.connect_retries})"
                    )
                    logger.warning(msg)
                    time.sleep(creds.connect_timeout)
                else:
                    logger.debug(f"failed to connect: {exc}")
                    _log_dbsql_errors(exc)
                    raise dbt.exceptions.FailedToConnectException("failed to connect") from e
        else:
            assert exc is not None
            raise exc

        connection.handle = handle
        connection.state = ConnectionState.OPEN
        return connection


def _log_dbsql_errors(exc: Exception) -> None:
    if isinstance(exc, DBSQLError):
        logger.debug(f"{type(exc)}: {exc}")
        for key, value in sorted(exc.context.items()):
            logger.debug(f"{key}: {value}")
