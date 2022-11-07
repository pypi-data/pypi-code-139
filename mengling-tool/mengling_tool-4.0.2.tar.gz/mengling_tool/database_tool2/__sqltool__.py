# -*- coding: UTF-8 -*-

import base64
import traceback
from threading import Thread
from pandas import DataFrame
from pyDes import PAD_PKCS5, CBC, des
from copy import deepcopy

__Des_Key0 = '%s&@W2*<FRW2'
__Des_IV = b'\x52\x63\x78\x61\xBC\x48\x6A\x07'


def encryption(user, passwd):
    k = des((__Des_Key0 % user)[:8], CBC, __Des_IV, padmode=PAD_PKCS5)
    return base64.b64encode(k.encrypt(passwd)).decode('utf-8')


def decrypt(user, passwd_enc):
    k = des((__Des_Key0 % user)[:8], CBC, __Des_IV, padmode=PAD_PKCS5)
    return k.decrypt(base64.b64decode(passwd_enc)).decode('utf-8')


# 表格去重
def table_drop_duplicates(dts: list, *lies) -> DataFrame:
    df = DataFrame(data=dts)
    df.drop_duplicates(subset=lies, keep='first', inplace=True)
    return df


# 模板工具
class TemplateSQLTool:
    def __init__(self, db_func, ifassert, iftz, default_lie_class='varchar(255)', default_where='true'):
        self.db_func = db_func
        self.ifassert = ifassert
        # 打开数据库连接
        self.db = db_func()
        self.cursor = self.db.cursor()
        self.default_lie_class = default_lie_class
        self.default_where = default_where

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # 刷新连接
    def refresh(self):
        self.close()
        self.db = self.db_func()
        self.cursor = self.db.cursor()

    # 使用sql操作
    def run(self, sql, datas=None, iftz=True, **kwargs):
        # print(sql)
        try:
            # 执行sql语句
            if datas is None:
                self.cursor.execute(sql)
            else:
                # datas中也为列表
                self.cursor.executemany(sql, datas if type(datas[0]) in (tuple, list) else [datas])
            return True
        except:
            print("\033[0;32m", sql, "\033[0m")
            if self.ifassert:
                if iftz:
                    print('datas:', str(datas)[:100], '...')
                raise ValueError(traceback.format_exc())
            elif iftz:
                print('datas:', str(datas)[:100], '...', '\n', traceback.format_exc())
            return False

    def close(self):
        try:
            self.db.close()
        except:
            pass

    '''事务操作'''

    # 提交事务
    def commit(self):
        self.db.commit()

    # 事务回滚
    def rollback(self):
        self.db.rollback()

    def getTablestr(self, table, **kwargs):
        return table

    def getLiestrs(self, lies, **kwargs):
        if type(lies) == str:
            if lies in {'*', '1', 'count(1)'}:
                return [lies]
            else:
                lies = [lies]
        lies = [f"`{lie}`" for lie in lies]
        return lies

    def getValuestrs(self, values, **kwargs):
        valuestrs = ["'%s'" % (str(value).replace("'", "\\'").strip()) for value in values]
        return valuestrs

    # 获取整合后的总列
    def getAllLies(self, dts):
        return DataFrame(data=dts).columns

    '''增删查改'''

    # 获取结果
    def getResult(self, data_class='dts'):
        # 获取数据
        lies = [lc[0] for lc in self.cursor.description] if self.cursor.description is not None else []
        result = list()
        for row in self.cursor.fetchall():
            dt = dict()
            for lie, data in zip(lies, row):
                dt[lie] = data
            result.append(dt)
        # 处理返回格式
        if data_class == 'ls':
            result = [list(dt.values()) for dt in result]
        elif data_class == 'df':
            result = DataFrame(data=result)
        return lies, result

    # 查询,会有事物隔离的情况出现,可以重新生成对象进行查询
    def select(self, lies, table, where=None, other='', data_class='dts', ifgetlies=False, ifget_one_lie=False,
               **kwargs):
        sql = '''select {lies}
                from {table}
                where {where}
                {other}
        '''.format(lies=','.join(self.getLiestrs(lies, **kwargs)), table=self.getTablestr(table, **kwargs),
                   where=where if where else self.default_where,
                   other=other)
        b = self.run(sql, **kwargs)

        if b:
            # 获取数据
            lies, result = self.getResult(data_class='ls' if ifget_one_lie else data_class)
            if ifget_one_lie: result = [d[0] for d in result]
        else:
            lies, result = None, None
        if ifgetlies:
            return lies, result
        else:
            return result

    # 判断是否可以查询到
    def ifGet(self, table, where=None, if_error=True, **kwargs):
        try:
            if len(self.select('1', table, where=where if where else self.default_where,
                               data_class='ls', other='limit 1',
                               iftz=False, **kwargs)) > 0:
                return True
            else:
                return False
        except:
            if if_error: traceback.print_exc()
            return False

    # 获取数量
    def getNum(self, table, where=None, **kwargs):
        num = self.select('count(1)', table, where=where if where else self.default_where, data_class='ls', iftz=False,
                          **kwargs)[0][0]
        return num

    # 插入
    def insert(self, table: str, lies: list, *all_values, ifyz=True, **kwargs):
        length = len(lies)
        assert length > 0, "列数量不能为0！"
        if ifyz:
            allvaluestrs = list()
            for values in all_values:
                assert len(values) == length, f'列数与值数不一致!{len(values)},{length}'
                allvaluestrs.append(tuple(map(lambda x: str(x).strip(), values)))
        else:
            allvaluestrs = all_values
        # 插入语句
        liestr = ','.join(self.getLiestrs(lies, **kwargs))
        sql = '''INSERT INTO {table}({liestr})
                VALUES ({cstr})
        '''.format(table=self.getTablestr(table, **kwargs), liestr=liestr,
                   cstr=','.join(['%s' for i in range(length)]))
        return self.run(sql, datas=allvaluestrs, **kwargs)

    # 批量插入字典,需要保证所有字典键值一致
    # 如果没有指定列,则会取第一个字典的列作为标准列,没有的部分其他字典会有默认值,但是多出的部分不会被记录
    def insert_create_dt(self, table: str, *dts, **kwargs):
        df = DataFrame(data=dts)
        return self.insert_create_df(table, df, **kwargs)

    def thread_insert_commit(self, table, dts, lies=None, columnclassdict: dict = None, key=None,
                             threadnum=10, ifcreate=True, **kwargs):
        if columnclassdict is None: columnclassdict = {}
        # 数据处理
        df = DataFrame(data=dts)
        df.fillna('', inplace=True)
        # 数据筛选
        lies = lies if lies is not None else list(df.columns)
        values = list()
        for index, row in df.iterrows():
            values.append([row.get(lie, '') for lie in lies])
        # 任务分配
        if ifcreate: self.createTable(table, lies, columnclassdict=columnclassdict, key=key, **kwargs)
        threadnum = min(threadnum, len(dts))
        length = len(dts) // threadnum
        threads = list()
        print('[线程插入数] %s' % threadnum)

        def temp(table, datas):
            conch = deepcopy(self.connect)
            conch['ifassert'] = True
            sqltool = type(self)(self.dbname, **self.connect)
            try:
                sqltool.insert(table, lies, *datas, ifcreate=False, ifyz=False, **kwargs)
                sqltool.commit()
            except:
                traceback.print_exc()
                print('出现错误,该批数据执行单条插入')
                for data in datas:
                    try:
                        sqltool.insert(table, data, lies=lies, ifcreate=False, ifyz=False, **kwargs)
                        sqltool.commit()
                    except:
                        print('[出错]', str(data)[:20], '...')
                        txt = traceback.format_exc()
                        print(txt.split('\n')[-1])
                        sqltool.rollback()
            sqltool.close()

        for i in range(threadnum):
            if i == threadnum - 1:
                values_ch = values[i * length:]
            else:
                values_ch = values[i * length:i * length + length]
            arg = [table, values_ch]
            t = Thread(target=temp, args=tuple(arg))
            t.start()
            threads.append(t)
        [t.join() for t in threads]

    def insert_create_df(self, table: str, df: DataFrame, lies=None,
                         columnclassdict: dict = None, key=None, ifcreate=True, **kwargs):
        # 数据处理
        df.fillna('', inplace=True)
        df.applymap(lambda x: str(x).strip())
        # 数据筛选
        lies = lies if lies is not None else list(df.columns)
        values = list()
        # 自动长度
        col_len = dict()
        for index, row in df.iterrows():
            ls = list()
            for lie in lies:
                ls.append(row[lie])
                if len(row[lie]) > 255:
                    col_len[lie] = 'text'
            values.append(ls)

        if ifcreate:
            # 更新自定义类型
            col_len.update(columnclassdict if columnclassdict else {})
            self.createTable(table, lies, columnclassdict=col_len, key=key, **kwargs)
        return self.insert(table, lies, *values, ifyz=False)

    # 删除
    def delete(self, table, where: str, **kwargs):
        # 表名
        sql = '''DELETE FROM {table}
            WHERE {where}
        '''.format(table=self.getTablestr(table, **kwargs), where=where)
        return self.run(sql, **kwargs)

    # 修改
    def update(self, table, lies: list, values: list, where: str, **kwargs):
        assert len(lies) > 0 and len(lies) == len(values), "数量有误！"
        setv = ','.join([(lie + "=%s") for lie in self.getLiestrs(lies, **kwargs)])
        sql = '''UPDATE {table}
                SET {setv}
                WHERE {where}
        '''.format(table=self.getTablestr(table, **kwargs), setv=setv, where=where)
        # print(sql)
        return self.run(sql, datas=values, **kwargs)

    def update_dt(self, table, dt: dict, where: str, **kwargs):
        lies, values = [], []
        for key, value in dt.items():
            lies.append(key)
            values.append(value)
        return self.update(table, lies, values, where, **kwargs)

    '''表操作'''

    # 创建表
    def createTable(self, table, lies: list, columnclassdict: dict = None, colmap: dict = None, key=None, **kwargs):
        # CREATE TABLE table_name (column_name column_type);  Create Table If Not Exists

        if columnclassdict is None and colmap is None:
            colmap = {}
        else:
            colmap = colmap if colmap is not None else columnclassdict
        assert len(lies) > 0, "数量有误！"
        # 列类型进行默认赋值
        for lie in lies:
            colmap[lie] = colmap.get(lie, self.default_lie_class)
        if key is not None:
            if type(key) == str: key = [key]
            if key != '*': key = " ,PRIMARY KEY(%s)" % ','.join(self.getLiestrs(key, **kwargs))
        else:
            key = ''
        # 不再使用null，默认为空字符
        liestr = ",".join([("%s %s " % (self.getLiestrs([lie], **kwargs)[0], colmap[lie]) +
                            ("NOT NULL DEFAULT ''" if 'varchar' in colmap[lie] else ''))
                           for lie in lies])
        sql = '''
            Create Table If Not Exists {table}
            ({lies} {key})
        '''.format(table=self.getTablestr(table, **kwargs), lies=liestr, key=key)
        return self.run(sql, **kwargs)

    # 删除表
    def deleteTable(self, table, **kwargs):
        # DROP TABLE table_name
        sql = '''DROP TABLE IF EXISTS {table} 
        '''.format(table=self.getTablestr(table, **kwargs))
        return self.run(sql, **kwargs)

    # 删除列
    def deleteColumn(self, table, liename, **kwargs):
        # ALTER TABLE tablename  DROP i;
        sql = '''ALTER TABLE {table} 
                DROP {liename}
        '''.format(table=self.getTablestr(table, **kwargs), liename=liename)
        return self.run(sql, **kwargs)

    # 修改列属性
    def setColumn(self, table, liename, newname, dataclass="VARCHAR(255)", **kwargs):
        lies = self.getLiestrs([liename, newname])
        sql = '''ALTER TABLE {table} 
                CHANGE {liename} {newname} {dataclass}
        '''.format(table=self.getTablestr(table, **kwargs), liename=lies[0], newname=lies[1], dataclass=dataclass)
        return self.run(sql, **kwargs)

    # 新增列
    def addColumn(self, table, liename, dataclass="VARCHAR(255)", other="", **kwargs):
        # ALTER TABLE `tcl科技 (深证:000100)` add `昨日收盘` VARCHAR(255) AFTER `今日收盘`
        sql = '''ALTER TABLE {table}
                ADD {liename} {dataclass} 
                {other}
        '''.format(table=self.getTablestr(table, **kwargs), liename=self.getLiestrs(liename)[0], dataclass=dataclass,
                   other=other)
        return self.run(sql, **kwargs)

    # 将表中所有字段的null替换为空字符,不推荐使用
    def replaceNULL(self, table):
        lies, datas = self.select('*', table)
        row_news = []
        for row in datas:
            row_news.append([d if d is not None else '' for d in row])
        # 清空表数据
        self.delete(table, 'True')
        [self.insert(table, lies, row) for row in row_news]
        self.commit()
