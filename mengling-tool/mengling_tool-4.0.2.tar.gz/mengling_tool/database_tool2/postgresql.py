# -*- coding: UTF-8 -*-

import psycopg2
from .__sqltool__ import TemplateSQLTool, decrypt


# postgresql执行类
class PostgresqlExecutor(TemplateSQLTool):
    def __init__(self, dbname: str, **connect):
        self.dbname = dbname
        self.connect = connect
        self.host = connect.get('host', '127.0.0.1')
        self.port = connect.get('port', 5432)
        self.user = connect.get('user', 'postgres')
        self.passwd = connect['password']
        self.charset = connect.get('charset', 'UTF8')
        ifassert = connect.get('ifassert', True)
        iftz = connect.get('iftz', False)
        self.ifencryption = connect.get('ifencryption', True)
        if self.ifencryption:
            self.passwd = decrypt(self.user, self.passwd)

        # 打开数据库连接
        def db_func():
            db = psycopg2.connect(host=self.host, port=self.port,
                                  user=self.user, password=self.passwd,
                                  database=self.dbname)
            db.set_client_encoding(self.charset)
            return db

        TemplateSQLTool.__init__(self, db_func, ifassert, iftz)

    def getTablestr(self, table, **kwargs):
        if '.' in table:
            t1, t2 = table.split('.')
            return f'"{t1}"."{t2}"'
        else:
            return f'"{table}"'

    def getLiestrs(self, lies, **kwargs):
        if type(lies) == str:
            if lies in {'*', '1', 'count(1)'}:
                return [lies]
            else:
                lies = [lies]
        lies = [f'"{lie}"' for lie in lies]
        return lies

    def getValuestrs(self, values, **kwargs):
        valuestrs = ["'%s'" % str(value).replace("'", "\\'").strip() for value in values]
        return valuestrs
