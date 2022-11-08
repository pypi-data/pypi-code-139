import pymssql
import pandas as pd

class SqlHandler():

    DEFAULT_SQL_DRIVER = '{ODBC Driver 18 for SQL Server}'

    def __init__(self):
        pass

    @property
    def conn():
        pass

    @conn.getter
    def conn(self) -> pymssql.Connection:
        """Database connection instance. Only valid after using '.connect_to_db'."""

        conn = getattr(self, '_conn', None)
        if not conn:
            raise ValueError(
                'Connection not yet established, use ".connect_to_db" first.'
            )

        return conn

    def connect_to_db(
            self, server: str, port: str, database: str, username: str, password: str, **kwargs) -> None:
        """
        Connects to the database, returning a pymssql connection instance.

        Warning: Uses TrustServerCertificate=yes, please ensure you're connecting to a secure db.

        :param server: The server URL (or local hosted string).
        :param database: The name of the database to connect to in the hosted instance.
        :param username: Client username to authenticate connection.
        :param password: Client password to authenticate connection.
        :param driver: Driver used to handle connection. Uses a sensible default, but modify if this doesn't work.
        :param **kwargs: Provide any additional kwargs for pymssql.connect (timeout for example).
        """

        if port and type(port) == int:
            port = str(port)

        self._conn = pymssql.connect(server=server, port=port, user=username, password=password, database=database, **kwargs)

        print('Connection to "{}" established'.format(database))

    @property
    def table_schemas():
        pass

    @table_schemas.getter
    def table_schemas(self) -> list:
        """List of all queriable table schemas the database."""

        with self.conn.cursor() as cur:
            table_schemas = [x[1] for x in cur.tables(tableType='TABLE')]

        return table_schemas

    @property
    def table_names():
        pass

    @table_names.getter
    def table_names(self) -> list:
        """List of all queriable table names in the database."""

        with self.conn.cursor() as cur:
            table_names = [x[2] for x in cur.tables(tableType='TABLE')]
            
        return table_names

    @property
    def table_schema_names():
        pass

    @table_schema_names.getter
    def table_schema_names(self) -> list:
        """List of all queriable table schemas and names joined as '{schema}.{name}'."""

        return ['{}.{}'.format(schema, name) for schema, name in zip(self.table_schemas, self.table_names)]

    def query(self, sql_string: str) -> pd.DataFrame:
        """Executes an SQL query, returning a dataframe of the result."""

        df = pd.read_sql_query(sql_string, self.conn)
        return df
