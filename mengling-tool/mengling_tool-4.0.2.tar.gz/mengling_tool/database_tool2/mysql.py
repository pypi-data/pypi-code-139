from threading import Thread
import pymysql
from .__sqltool__ import TemplateSQLTool, decrypt


# mysql执行类
class MysqlExecutor(TemplateSQLTool):
    def __init__(self, dbname: str, default_lie_class='varchar(255)', **connect):
        self.dbname = dbname
        self.connect = connect
        self.host = connect.get('host', '127.0.0.1')
        self.port = connect.get('port', 3306)
        self.user = connect.get('user', 'root')
        self.passwd = connect['password']
        self.charset = connect.get('charset', 'utf8mb4')
        ifassert = connect.get('ifassert', True)
        iftz = connect.get('iftz', True)
        self.ifencryption = connect.get('ifencryption', True)
        if self.ifencryption: self.passwd = decrypt(self.user, self.passwd)
        # 打开数据库连接
        db_func = lambda :pymysql.connect(host=self.host, port=self.port,
                                  user=self.user, passwd=self.passwd,
                                  db=self.dbname, charset=self.charset)
        TemplateSQLTool.__init__(self, db_func, ifassert, iftz,
                                 default_lie_class=default_lie_class)

    def run(self, sql, **kwargs):
        # 设置重连
        self.db.ping(reconnect=True)
        return TemplateSQLTool.run(self, sql, **kwargs)

    def commit(self):
        # 设置重连
        self.db.ping(reconnect=True)
        return TemplateSQLTool.commit(self)

    def getTablestr(self, table, **kwargs):
        return '`%s`' % table

    def getLiestrs(self, lies, **kwargs):
        if type(lies) == str:
            if lies in {'*', '1', 'count(1)'}:
                return [lies]
            else:
                lies = [lies]
        lies = [f"`{lie.replace('%', '%%')}`" for lie in lies]
        return lies

    def createTable(self, table, lies: list, columnclassdict: dict = None, key=None, ifmyisam=False, **kwargs):
        if columnclassdict is None: columnclassdict = {}
        b = TemplateSQLTool.createTable(self, table, lies, columnclassdict=columnclassdict, key=key)
        # 使用MyISAM引擎具有更强的读写速度,但是不支持事物
        if ifmyisam: self.run(f'ALTER TABLE {self.getTablestr(table)} ENGINE = MyISAM')
        return b

    # 添加索引
    def addIndex(self, table, index_name, index_lie):
        self.run(f'ALTER TABLE {self.getTablestr(table)} ADD INDEX `{index_name}`(`{index_lie}`);')

    # 分割表,不建议使用
    def divisionTable(self, table, sqlcellnum=50_0000, columnclassdict: dict = None, threadnum=10):
        if columnclassdict is None:
            columnclassdict = {}
        # 获取最大数量
        maxlen = self.run(f"select count(1) from `{table}`", ifdatas=True)[1][0][0]

        def temp(iss):
            sqltool = MysqlExecutor(self.dbname, **self.connect)
            for i in iss:
                lies, datas = sqltool.select('*', table, other=f"limit {i},{sqlcellnum}")
                # if len(datas) == 0: break
                newtable = f'{table}_{i}'
                sqltool.createTable(newtable, lies, columnclassdict=columnclassdict, ifmyisam=True)
                sqltool.insert(newtable, lies, *datas)
                print(i)
            sqltool.close()

        iss = [i for i in range(0, maxlen, sqlcellnum)]
        tasklen = len(iss)
        if tasklen == 0: return
        num = min(threadnum, tasklen)
        cellnum = tasklen // num if tasklen % num == 0 else tasklen // num + 1
        ts = list()
        for i in range(0, tasklen, cellnum):
            t = Thread(target=temp, args=(iss[i:i + cellnum],))
            t.start()
            ts.append(t)
        [t.join() for t in ts]

    def ifExist(self, table):
        b = self.run(f'show tables like "{table}"')
        return b and len(self.cursor.fetchall()) > 0


# 测试
if __name__ == "__main__":
    pass
