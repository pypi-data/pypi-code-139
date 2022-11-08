# -*- coding: utf-8 -*-
import datetime
import psycopg2.extras
import psycopg2 as pg
import MySQLdb
import requests
import json
import urllib
import hmac
import base64
import hashlib
import sys
import time
import io
reload(sys)
sys.setdefaultencoding('utf-8')
# python 2.7安装 mysql-python
# pip install psycopg2-binary


def test():
    print('test')


class Mysql2Pg:

    def __init__(self, parameter_json):
        """
        :param parameter_json: json类型的参数，*是必须项
        {
        * read_config json
            {
            * config json: 数据库连接
            * table_name str: 数据库的表
            field_list []: 字段列表，默认全部
            read_batch int: 每次最多获取"对应条数"的数据，处理后，再继续获取对应条数的数据处理，以此循环
            increment_col str: 增量同步的列，为空时表示全量查询；有值时从write从查询改字段最大值进行增量同步
            }
        * write_config json
            {
            * config json: 数据库连接
            * table_name str: 数据库的表
            is_field_fix int: 默认0; 字段同步，1和read字段一致(会增删字段),0不作字段处理
            field_list []: 默认和read字段的交集; 写入的字段列表
            write_batch int: 默认2000; 将相应数量的insert组合成一个大insert进行写入
            is_truncate int: 默认0; 0增量写入，1全量写入(会truncate表)
            end_sql str: 结束后执行的sql
            }
        * data json
            {
            user_bot json : 用户接收消息，由用户传入
                {
                bot_url str: 机器人url，用于通知进度
                bot_secret str: 机器人加签，用于通知进度
                }
            root_bot json : 管理员接受消息，有默认值
                {
                bot_url str: 机器人url，用于通知进度
                bot_secret str: 机器人加签，用于通知进度
                }
            }
        }

        """
        self.result_dict = dict()  # 关键信息的返回

        # self.read_db_config = read_db_config
        # self.write_db_config = write_db_config
        self.parameter_json = parameter_json
        # self.check_par()
        # self.is_bot = 1 if parameter_json.get('data').get('bot_url') else 0
        self.intersection_col = list()
        self.read_db_config = parameter_json.get('read_config').get('config')
        self.read_table_name = parameter_json.get('read_config').get('table_name')
        self.increment_col = parameter_json.get('read_config').get('increment_col')
        self.read_batch = parameter_json.get('read_config').get('read_batch')
        if self.read_batch is None:
            self.read_batch = 5000
        self.write_db_config = parameter_json.get('write_config').get('config')
        self.write_table_name = parameter_json.get('write_config').get('table_name')
        self.write_is_truncate = parameter_json.get('write_config').get('is_truncate')
        self.grant_select = parameter_json.get('write_config').get('grant_select')
        self.index_field = parameter_json.get('write_config').get('index_field')
        self.write_batch = parameter_json.get('write_config').get('write_batch')
        if self.write_batch is None:
            self.write_batch = 5000
        if self.write_is_truncate is None or self.write_is_truncate == '':
            self.write_is_truncate = 0

        self.task_id = '0'
        self.root_bot_url = ''
        self.root_bot_secret = ''
        self.user_bot_url = ''
        self.user_bot_secret = ''
        self.user_bot_at_mobiles = list()
        self.full_fire = 0
        self.ct = ''

        self.default_bot_url = ''
        self.default_bot_sec = ''
        self.is_full_msg = '0'

        if parameter_json.get('data'):
            self.ct = parameter_json.get('data').get('ct')
            self.is_full_msg = parameter_json.get('data').get('is_full_msg')
            if parameter_json.get('data').get('full_fire')=='1':
                self.full_fire = 1
            if parameter_json.get('data').get('root_bot'):
                self.root_bot_url = parameter_json.get('data').get('root_bot').get('bot_url')
                self.root_bot_secret = parameter_json.get('data').get('root_bot').get('bot_secret')
                self.user_bot_url = parameter_json.get('data').get('user_bot').get('bot_url')
                self.user_bot_secret = parameter_json.get('data').get('user_bot').get('bot_secret')
                self.user_bot_at_mobiles = parameter_json.get('data').get('user_bot').get('at_mobiles')
            if parameter_json.get('data').get('default_bot'):
                self.default_bot_url = parameter_json.get('data').get('default_bot').get('bot_url')
                self.default_bot_sec = parameter_json.get('data').get('default_bot').get('bot_secret')
            if parameter_json.get('data').get('task_id'):
                self.task_id = parameter_json.get('data').get('task_id')

        self.write_cnt = 0  # 写入的数量

    def start(self):
        start_time = self.get_timestamp()
        start_unix = self.get_timestamp(time_type='unix')
        self.result_dict['task_id'] = self.task_id

        # ------- 任务开始 -------
        extract_type = '%s 增量' % self.increment_col if self.increment_col else '全量'
        task_table = '"%s" ->> "%s"' % (self.read_table_name, self.write_table_name)
        start_msg = '**%s-<font color=#28004D> 开始同步 </font>**  \n%s  \n> <font color=#272727> task_id </font>: %s  \n' \
                    '> <font color=#272727> 同步方式 </font>: %s  ' \
                    % (self.ct, task_table, self.task_id, extract_type)
        # 发送开始消息
        self._info_msg(start_msg, level=1, msg_type='markdown')
        self.result_dict['start_msg'] = start_msg

        # -------  检查表结构  -------
        core_msg_list = self._check_tab(task_table)
        self.result_dict['check_tab'] = ';'.join(core_msg_list)

        # -------  数据同步 -------
        trans_num = self._data_trans()
        exe_second = self.get_timestamp(time_type='unix')-start_unix
        end_msg = '**%s-<font color=#EA0000> 完成 </font>**  \n%s  \n> <font color=#272727> task_id </font>: %s  \n' \
                  '> <font color=#272727> 同步数量 </font>: %s  \n<font color=#272727> 同步时间 </font>: %s s  ' \
                  % (self.ct, task_table, self.task_id, trans_num, exe_second)
        self.result_dict['end_msg'] = end_msg
        self.result_dict['write_cnt'] = self.write_cnt  # 写入的数据量
        self.result_dict['read_cnt'] = trans_num  # 读取的数据量

        self.result_dict['url'] = self.user_bot_url
        self.result_dict['sec'] = self.user_bot_secret
        self._info_msg(end_msg, level=1, msg_type='markdown')

        # if self.user_bot_at_mobiles:
        self._info_msg('%s \n%s 已同步完成' % (self.ct, self.write_table_name), level=1, msg_type='text',
                       is_at_user=1,
                       msg_diff='remind')
        return self.result_dict

    def err(self, msg):
        raise ValueError(msg)

    @staticmethod
    def _datatype_mysql2pg(mysql_datatype):
        mysql_datatype = mysql_datatype.lower()
        pg_int = ['int', 'tinyint', 'smallint', 'year']
        pg_bigint = ['mediumint', 'bigint']
        pg_numeric = ['float', 'double', 'decimal']
        pg_text = ['varchar', 'char', 'tinytext', 'text', 'mediumtext', 'longtext']
        pg_timestamp = ['timestamp', 'datetime']
        pg_date = ['date']
        other = 'text'
        """
        Boolean	bit, bool
        Bytes	tinyblob, mediumblob, blob, longblob, varbinar
        """
        if any(i in mysql_datatype for i in pg_bigint):
            return 'bigint'
        if any(i in mysql_datatype for i in pg_int):
            return 'int'
        if any(i in mysql_datatype for i in pg_numeric):
            return 'numeric'
        if any(i in mysql_datatype for i in pg_text):
            return 'text'
        if any(i in mysql_datatype for i in pg_timestamp):
            return 'timestamp'
        if any(i in mysql_datatype for i in pg_date):
            return 'date'
        return other

    # python 2.7安装 mysql-python
    @staticmethod
    def dingding_msg(url, secret, msg, msg_type='text', is_at_user=0, at_mobiles=None):
        # if is_at_user == 1 and len(at_mobiles) > 0:
        #     msg = "%s  \n%s" % (msg, ' @%s'.join(at_mobiles))
        # else:
        #     at_mobiles = []
        _ver = sys.version_info
        is_py3 = (_ver[0] == 3)
        start_time = time.time()
        if secret is not None and secret.startswith('SEC'):
            if is_py3:
                timestamp = round(start_time * 1000)
                string_to_sign = '{}\n{}'.format(timestamp, secret)
                hmac_code = hmac.new(secret.encode(), string_to_sign.encode(), digestmod=hashlib.sha256).digest()
            else:
                timestamp = long(round(start_time * 1000))
                secret_enc = bytes(secret).encode('utf-8')
                string_to_sign = '{}\n{}'.format(timestamp, secret)
                string_to_sign_enc = bytes(string_to_sign).encode('utf-8')
                hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()

            sign = urllib.quote_plus(base64.b64encode(hmac_code))
            url = "%s&timestamp=%s&sign=%s" % (url, str(timestamp), sign)

            headers = {"Content-Type": "application/json;charset=utf-8"}

            if msg_type == 'markdown':
                data = {"msgtype": msg_type, "markdown": {"title": "msg", "text": msg}}
            else:
                data = {"msgtype": 'text', "text": {"content": msg}, "at": {"atMobiles": at_mobiles}}
            bot_result = requests.post(url, data=json.dumps(data), headers=headers)
            print(bot_result.text)

    # noinspection PyBroadException
    def _data_trans(self):

        if self.increment_col is not None and self.increment_col != '' and self.increment_col in self.intersection_col:
            # 有增量
            with pg.connect(**self.write_db_config) as conn:
                cur = conn.cursor(cursor_factory=pg.extras.RealDictCursor)
                cur.execute(
                    """select coalesce(max(%s),0) max_inc from %s;""" % (self.increment_col, self.write_table_name))
                max_inc = cur.fetchall()[0].get('max_inc')
                self._info_msg(max_inc)
            read_sql = 'select %s from %s where %s>%s;' % ('`%s`' % '`,`'.join(self.intersection_col), self.read_table_name
                                                           , self.increment_col, max_inc)
            read_sql_log = 'select - from %s where %s>%s;' % (self.read_table_name,
                                                              self.increment_col, max_inc)
        else:
            read_sql = 'select %s from %s ;' % ('`%s`' % '`,`'.join(self.intersection_col), self.read_table_name)
            read_sql_log = 'select - from %s ;' % self.read_table_name
            self.write_is_truncate = 1  # 全量时重新赋值，预防"期望增量同步，但增量字段在表中不存在后跳转到全量同步的情况"
        self._info_msg('read_sql: %s' % read_sql_log)

        # TODO 兼容pg列名长度63的部分问题
        copy_column = tuple(self.intersection_col)
        write_conn = pg.connect(**self.write_db_config)
        read_conn = MySQLdb.connect(**self.read_db_config)
        try:
            # ------ 目标数据库对象（写入数据）------
            write_cur = write_conn.cursor(cursor_factory=pg.extras.RealDictCursor)
            if self.write_is_truncate == 1:
                # 全量同步：清空表
                truncate_sql = "truncate table %s;" % self.write_table_name
                write_cur.execute(truncate_sql)
                write_conn.commit()
                self._info_msg("执行sql: %s" % truncate_sql)

            # ------ 源数据库对象（拉取数据）------
            # （SSCursor + itersize）流的形式批次拉取，避免资源问题和耗时过长问题
            read_cursor = read_conn.cursor(cursorclass=MySQLdb.cursors.SSCursor)
            read_cursor.itersize = self.read_batch
            read_cursor.execute(read_sql)
            batch_index = 0
            batch_sql = list()
            for read_rows in read_cursor:
                if batch_index % self.write_batch == 0 and batch_index > 0:
                    batch_sql.append(read_rows)
                    self.write_cnt += len(batch_sql)
                    write_pg_obj = self.WritePg(self.full_fire)
                    write_pg_obj.write_copy(write_conn, self.write_table_name, batch_sql, size=8192,
                                            column=copy_column)
                    del write_pg_obj
                    write_conn.commit()
                    # self._info_msg('批量写入: %s' % batch_index)
                    del batch_sql
                    batch_sql = list()
                else:
                    batch_sql.append(read_rows)
                batch_index += 1
            if batch_sql:
                self.write_cnt += len(batch_sql)
                write_pg_obj = self.WritePg(self.full_fire)
                write_pg_obj.write_copy(write_conn, self.write_table_name, batch_sql, size=8192,
                                        column=copy_column)
                del write_pg_obj
                write_conn.commit()
                self._info_msg('批量写入: %s' % batch_index)
            write_conn.close()
            read_conn.close()

        except Exception as e:
            write_conn.commit()
            read_conn.close()
            write_conn.close()
            raise ValueError('write error:[ %s--%s ] %s' % (self.ct, self.write_table_name, str(e)))
        return batch_index

    def _check_tab(self, task_table='?->?'):
        core_msg_list = list()
        read_db_config = self.read_db_config
        read_table_name = self.read_table_name
        write_db_config = self.write_db_config
        write_table_name = self.write_table_name

        # read表结构
        conn = MySQLdb.connect(**read_db_config)
        cur = conn.cursor(
            MySQLdb.cursors.DictCursor)
        read_sql = """select lower(column_name) as column_name,lower(data_type) as data_type
            from information_schema.columns
            where table_schema='%s' and table_name='%s'
            """ % (read_table_name.split('.')[0], read_table_name.split('.')[1])
        cur.execute(read_sql)
        read_col_kv_list = list(cur.fetchall())
        conn.close()
        None if read_col_kv_list else self.err("table not found: [%s]" % read_table_name)

        # 将字段名改为小写（统一格式）
        new_list = list()
        for kv in read_col_kv_list:
            new_dict = {}
            for i, j in kv.items():
                new_dict[i.lower()] = j
            new_list.append(new_dict)
        read_col_kv_list = new_list

        read_field_list = [i.get('column_name') for i in read_col_kv_list]

        # write表结构
        with pg.connect(**write_db_config) as conn:
            cur = conn.cursor(cursor_factory=pg.extras.RealDictCursor)
            cur.execute("""select column_name,data_type 
                from information_schema.columns 
                where table_schema='%s' and table_name='%s'
                """ % (write_table_name.split('.')[0], write_table_name.split('.')[1]))
            write_field_list = list()
            write_col_kv_list = cur.fetchall()
            is_table = 1 if write_col_kv_list else 0  # 表是否存在
            for i in write_col_kv_list:
                write_field_list.append(i.get('column_name'))

        #  ------------------ 表不存在的处理 ------------------
        #  生成建表语句：创建索引字段 和 赋权
        if is_table == 0:
            field_list = list()
            for i in read_col_kv_list:
                field_list.append("%s %s" % (i.get('column_name'), self._datatype_mysql2pg(i.get('data_type'))))
            field_str = ',\n  '.join(field_list)

            # 建表语句
            create_sql = "create table {table} (\n  {field} \n);".format(table=write_table_name, field=field_str)
            # self._info_msg('[%s] create table: %s' % (self.ct, write_table_name), level=2)
            core_msg_list.append('> <font color=#272727> create table </font>: %s' % self.write_table_name)

            # 索引
            index_sql_list = list()
            create_index_field = list()
            index_field = self.index_field if self.index_field else ['id', 'serial_id', 'create_time']
            for i in read_field_list:
                if i in index_field:
                    index_sql_list.append("create index idx_{table_name}_{field} on {table}({field});".format(
                        field=i, table=write_table_name, table_name=write_table_name.replace('.', '_')))
                    create_index_field.append(i)
            index_sql = '\n'.join(index_sql_list)
            # self._info_msg(index_sql)
            core_msg_list.append('> <font color=#272727> 创建索引字段 </font>: %s' % ','.join(create_index_field))

            # 赋权
            # grant_select = self.grant_select if self.grant_select else 'read_user'
            grant_sql = ''
            if self.grant_select:
                grant_sql = 'grant select on {table} to {user};'.format(table=write_table_name, user=self.grant_select)
                # self._info_msg(self.grant_select)
                core_msg_list.append('> <font color=#272727> 赋权 </font>: %s' % self.grant_select)
            else:
                # self._info_msg('[%s] %s no grant' % (self.ct, self.write_table_name), 2)
                pass

            # 执行sql
            with pg.connect(**write_db_config) as conn:
                cur = conn.cursor(cursor_factory=pg.extras.RealDictCursor)
                cur.execute(create_sql)
                if index_sql != '' and index_sql is not None:
                    cur.execute(index_sql)
                if grant_sql != '' and grant_sql is not None:
                    cur.execute(grant_sql)
                conn.commit()
            self.intersection_col = read_field_list

        #  ------------------ 表已存在的处理 ------------------
        # 字段不匹配的处理
        if is_table == 1:
            self._info_msg('表存在')
            intersection_col = (list(set(read_field_list).intersection(set(write_field_list))))
            self.intersection_col = intersection_col
            alter_sql_list = list()
            add_field_list = list()
            delete_field_list = list()
            # TODO 兼容pg列名长度63的部分问题
            for kv in read_col_kv_list:
                if kv.get('column_name') not in intersection_col:
                    add_field_list.append(kv.get('column_name'))
                    # self._info_msg('增加字段: %s' % kv.get('column_name'))
                    alter_sql_list.append("alter table %s add column %s %s;"
                                          % (write_table_name, kv.get('column_name')
                                             , self._datatype_mysql2pg(kv.get('data_type')))
                                          )
                    intersection_col.append(kv.get('column_name'))

            for kv in write_col_kv_list:
                if kv.get('column_name') not in intersection_col:
                    delete_field_list.append(kv.get('column_name'))
                    # self._info_msg('删除字段: %s' % kv.get('column_name'))
                    alter_sql_list.append("alter table %s drop column %s;"
                                          % (write_table_name, kv.get('column_name'))
                                          )
            if alter_sql_list:
                core_msg_list.append('> <font color=#272727> 增加字段 </font>: %s' % ','.join(add_field_list))
                core_msg_list.append('> <font color=#272727> 删除字段 </font>: %s' % ','.join(delete_field_list))
                alter_sql = '\n'.join(alter_sql_list)
                # 执行sql
                with pg.connect(**write_db_config) as conn:
                    cur = conn.cursor(cursor_factory=pg.extras.RealDictCursor)
                    cur.execute(alter_sql)
                    conn.commit()

        if len(core_msg_list) == 0:
            # -- 调整：表结构物无变更时不再发送通知，避免消息过多
            pass
            # core_msg_list.append('> <font color=#FF0000> 表检查 </font>: 无需处理')
            # self._info_msg('**%s**  \n%s  \n> <font color=#FF0000> task_id </font>: %s  \n%s'
            #                % (self.ct, task_table, self.task_id, '  \n'.join(core_msg_list))
            #                , level=1, msg_type='markdown')
        else:
            self._info_msg('**%s**  \n%s  \n> <font color=#272727> task_id </font>: %s  \n%s'
                           % (self.ct, task_table, self.task_id, '  \n'.join(core_msg_list))
                           , level=2, msg_type='markdown')
        return core_msg_list

    @staticmethod
    def get_timestamp(day=0, utc=8, time_type='timestamp'):
        # 获取当前时间timestamp
        now_time = int(time.time()) + (day * 86400)  # 当前对应的时间戳
        utc_time = datetime.datetime.utcfromtimestamp(now_time + utc * 3600)
        if time_type == 'unix':
            return now_time
        return utc_time.strftime("%Y-%m-%d %H:%M:%S")

    def set_logfile(self, file_path):
        pass

    def _info_msg(self, msg, level=0, msg_type='text', is_at_user=0, msg_diff=''):
        """
        :param level:
            :: 0、消息打印, 不需要机器人通知
            :: 1、正常的消息通知, 如任务的开始和结束
            :: 2、关键的消息通知, 如表结构更改
            :: 3、重要的消息通知, 需要发现消息后紧急处理
        """
        msg = '%s -- %s' % (self.get_timestamp(), msg)
        print(msg)

        if 1 <= level <= 3:
            if self.is_full_msg == '0':
                if msg_diff == 'remind':
                    if self.user_bot_url:
                        self.dingding_msg(self.user_bot_url, self.user_bot_secret, msg=msg, msg_type=msg_type
                                     , is_at_user=is_at_user, at_mobiles=self.user_bot_at_mobiles)
                else:
                    if self.default_bot_url:
                        self.dingding_msg(self.default_bot_url, self.default_bot_sec, msg=msg, msg_type=msg_type)
            else:
                if self.user_bot_url:
                    self.dingding_msg(self.user_bot_url, self.user_bot_secret, msg=msg, msg_type=msg_type
                                 , is_at_user=is_at_user, at_mobiles=self.user_bot_at_mobiles)
        if level >= 2:
            if self.root_bot_url:
                self.dingding_msg(self.root_bot_url, self.root_bot_secret, msg=msg, msg_type=msg_type
                             , is_at_user=is_at_user)

    class StringIteratorIO(io.TextIOBase):
        def __init__(self, iter):
            self._iter = iter
            self._buff = ''

        def readable(self):
            return True

        def _read1(self, n):
            while not self._buff:
                try:
                    self._buff = next(self._iter)
                except StopIteration:
                    break
            ret = self._buff[:n]
            self._buff = self._buff[len(ret):]
            return ret

        def read(self, n):
            line = []
            if n is None or n < 0:
                while True:
                    m = self._read1()
                    if not m:
                        break
                    line.append(m)
            else:
                while n > 0:
                    m = self._read1(n)
                    if not m:
                        break
                    n -= len(m)
                    line.append(m)
            return ''.join(line)

    class WritePg:
        def __init__(self, full_fire=0):
            self.full_fire = full_fire
            pass

        def write_copy(self, connection, table_name, beers, size=8192, column=None):
            with connection.cursor() as cursor:
                beers_string_iterator = self.StringIteratorIO((
                    '\t'.join(map(self.clean_csv_value
                                  , beer
                                  )) + '\n'
                    for beer in beers
                ))
                cursor.copy_from(beers_string_iterator, table_name, sep='\t', size=size, columns=column, null='')
                # print('copy耗时： %s' % (in:t(time.time()) - s))

        def clean_csv_value(self, value):
            if value is None:
                return ''
            if self.full_fire == 1:
                return str(value)
            # return str(value).replace('\\0', "").replace('\x00', "").replace('\\', '\\\\')\
            #     .replace('\r', "\\r").replace('\n', '\\n').replace('\t', "\\t").replace('^', '')
            # ----- 下面的方式，会导致内存一直增加  -----
            # return str(value).encode('unicode-escape').decode('utf8').replace('\\\\0', '')\
            #     .replace('\\x00', '').replace('^', '')
            return str(value).replace('\\0', "").replace('\x00', "").replace('\\', '\\\\') \
                .replace('\r', "\\r").replace('\n', '\\n').replace('\t', "\\t").replace('\b', "\\b").replace('\f',
                                                                                                             "\\f") \
                .replace('\a', "\\a").replace('\v', '\\v').replace('\'', "\\'").replace('\"', '\\"').replace('\0', "") \
                .replace('\000', '')  # .replace('^', '')
