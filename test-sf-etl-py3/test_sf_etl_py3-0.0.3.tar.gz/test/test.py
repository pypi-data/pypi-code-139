# -*- coding: utf-8 -*-
from sf_etl_py3 import Bot
import json
import psycopg2.extras
import psycopg2 as pg
import ast

pg_config = {'host': 'rm-t4ne89z027r9mrz419o.pgsql.singapore.rds.aliyuncs.com', 'port': 3433, 'user': 'etl_user', 'password': 'temp4you', 'database': 'dw'}
pg_config_json = str(pg_config)
print(pg_config_json)
if isinstance(pg_config_json, str):
    pg_config_json = ast.literal_eval(pg_config_json)
pg_sql = 'select * from dim.user limit 2;'
access_key_id = 'LTAI5tKYoVtLXzZ8s7QCidwa'
access_key_secret = 'tv0Mo0KTs6yih251tSubteqaS253ue'


a = Bot.DingBot()
a.set_kwargs(url='https://oapi.dingtalk.com/robot/send?access_token=9e225e7be6a88f4585592954ab9acf8ed8075f810b81cfd06b600a6d0b1a93a4',
             sec='SECe10e3e6ab6a9efb8920040b10a9121800e8d7bf5c1a0380d4fc5e000fd4b5fb0',
             access_key_id=access_key_id,
             access_key_secret=access_key_secret)
a.append_bot_msg('test')
a.append_bot_msg('22')
r = a.send_img_simple(pg_config, pg_sql)
print(r.text)


