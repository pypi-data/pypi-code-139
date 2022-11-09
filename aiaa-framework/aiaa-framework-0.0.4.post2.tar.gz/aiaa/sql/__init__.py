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

    def connect_to_db(self, **kwargs) -> None:
        """
        Connects to the database, returning a pymssql connection instance.

        Recommended:
        :param server: The server URL (or local hosted string).
        :param port: The port to use for connecting to the server.
        :param database: The name of the database to connect to in the hosted instance.
        :param user: Client username to authenticate connection.
        :param password: Client password to authenticate connection.
        """

        self._conn = pymssql.connect(**kwargs)
        print('Connection established')

    def query(self, sql_string: str) -> pd.DataFrame:
        """Executes an SQL query, returning a dataframe of the result."""

        df = pd.read_sql_query(sql_string, self.conn)
        return df


    '''
    The following is broken moving from pyodbc -> pymssql:

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

    '''