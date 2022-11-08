# from yourtools.WeChat import WeChat
from yourtools import WeChat
from yourtools import MySQL
from yourtools import Hive


def test_wechat():
    # 仲达（测试）
    zd_test = WeChat("ww06fa03084e27ff22", "uwYEfV7eyDL1y3IzkD_RvksxiA5UBvmJzWNP4ze8vjU", 1000116)
    data = {
        "touser": "1331811502877461564",
        "toparty": "",
        "totag": "",
        "msgtype": "text",
        "agentid": 1000116,
        "text": {
            "content": "你的快递已到，请携带工卡前往邮件中心领取。\n出发前可查看<a href=\"http://work.weixin.qq.com\">邮件中心视频实况</a>，聪明避开排队。"
        },
        "safe": 0,
        "enable_id_trans": 0,
        "enable_duplicate_check": 0,
        "duplicate_check_interval": 1800
    }
    send_statu = zd_test.send_msg(data)
    print(send_statu)


def test_mysql():
    dbconfg = {
        'host': '127.0.0.1',
        'port': 3308,
        'username': 'root',
        'password': '*****',
        'db': 'test',
        'charset': 'utf8'
    }
    mysql = MySQL(dbconfg)
    # result = mysql.execute("insert into users_cdc(name,birthday,ts) values('灭霸2','2022-11-01 16:00:00','2022-11-01 16:00:00') ")
    result = mysql.query("select * from users_cdc")
    print(result)


def test_dml_mysql():
    # 默认测试连接的数据库
    dev_db_config = {
        'host': '127.0.0.1',
        'username': 'root',
        'password': '*****',
        'port': 13338,
        'db': 'datahub',
        'charset': 'utf8mb4'
    }

    dev_mysql = MySQL(db_config=dev_db_config)
    config = '{"filters":[{"key":"CD4CEBB1","name":"医院","multiple":true,"type":"treeSelect","cache":true,"expired":300,"width":0,"visibility":"visible","operator":"in","optionType":"manual","valueViewId":22,"valueField":"id","parentField":"parent_code","textField":"dpt_name","defaultValueType":"fixed","defaultValue":null,"relatedItems":{"122":{"viewId":71,"checked":true},"123":{"viewId":72,"checked":true},"124":{"viewId":73,"checked":true},"125":{"viewId":74,"checked":true},"907":{"viewId":893,"checked":true},"909":{"viewId":894,"checked":true},"1084":{"viewId":1058,"checked":true}},"relatedViews":{"71":{"fieldType":"column","fields":["医院编码"]},"72":{"fieldType":"column","fields":["医院编码"]},"73":{"fieldType":"column","fields":["医院编码"]},"74":{"fieldType":"column","fields":["医院编码"]},"893":{"fieldType":"column","fields":["医院编码"]},"894":{"fieldType":"column","fields":["医院编码"]},"1058":{"fieldType":"column","fields":["医院编码"]}}},{"key":"27EF3894","name":"医院状态","multiple":true,"type":"select","cache":false,"expired":300,"width":0,"visibility":"visible","operator":"in","optionType":"auto","defaultValueType":"fixed","relatedItems":{"122":{"viewId":71,"checked":true},"123":{"viewId":72,"checked":true},"124":{"viewId":73,"checked":true},"125":{"viewId":74,"checked":true},"907":{"viewId":893,"checked":false},"909":{"viewId":894,"checked":false},"1084":{"viewId":1058,"checked":false}},"relatedViews":{"71":{"fieldType":"column","fields":["医院状态"]},"72":{"fieldType":"column","fields":["医院状态"]},"73":{"fieldType":"column","fields":["医院状态"]},"74":{"fieldType":"column","fields":["医院状态"]}}},{"key":"26AD19A6","name":"日期","type":"dateRange","width":6,"visibility":"visible","defaultValueType":"dynamic","dateFormat":"YYYY-MM-DD","defaultValue":[{"type":"day","valueType":"prev","value":1},{"type":"day","valueType":"prev","value":1}],"relatedItems":{"122":{"viewId":71,"checked":true},"123":{"viewId":72,"checked":false},"124":{"viewId":73,"checked":true},"125":{"viewId":74,"checked":false},"907":{"viewId":893,"checked":true},"909":{"viewId":894,"checked":true},"1084":{"viewId":1058,"checked":true}},"relatedViews":{"71":{"fieldType":"variable","fields":["start_dt","end_dt"]},"73":{"fieldType":"variable","fields":["start_dt","end_dt"]},"893":{"fieldType":"variable","fields":["start_dt","end_dt"]},"894":{"fieldType":"variable","fields":["start_dt","end_dt"]},"1058":{"fieldType":"variable","fields":["start_dt","end_dt"]}}},{"key":"16A3F071","name":"账单时间类型","type":"select","width":0,"visibility":"visible","defaultValueType":"fixed","multiple":true,"cache":false,"expired":300,"operator":"in","optionType":"custom","customOptions":[{"value":"账单时间＞6个月","text":"账单时间＞6个月"},{"value":"3个月＜账单时间≤6个月","text":"3个月＜账单时间≤6个月"},{"value":"1个月＜账单时间≤3个月","text":"1个月＜账单时间≤3个月"},{"value":"48h＜账单时间≤1个月","text":"48h＜账单时间≤1个月"},{"value":"账单时间≤48h","text":"账单时间≤48h"}],"relatedItems":{"122":{"viewId":71,"checked":true},"123":{"viewId":72,"checked":false},"124":{"viewId":73,"checked":true},"125":{"viewId":74,"checked":false},"907":{"viewId":893,"checked":false},"909":{"viewId":894,"checked":false}},"relatedViews":{"71":{"fieldType":"column","fields":["账单时间类型"]},"73":{"fieldType":"column","fields":["账单时间类型"]}}}],"linkages":[],"queryMode":1}'
    result = dev_mysql.execute(
        "update davinci.dashboard set config='{config}' where id = {dashboard_id}".format(config=config,
                                                                                          dashboard_id=707))
    print(result)


def test_hive():
    hive_connection = {
        'host': 'emr-header-2',
        'port': 10000,
        'db': 'ods',
        'username': '',
        'auth': 'NOSASL'
    }
    hive = Hive(hive_connection)
    # hive_sql = """
    # select count(*) from dim.dim_clinic
    # """
    # rows = hive.query(hive_sql)
    # print(rows)

    sql2 = "use ods"
    result = hive.exec_ddl_sql(sql2)
    print(result)


def main():
    test_dml_mysql()


if __name__ == '__main__':
    main()
