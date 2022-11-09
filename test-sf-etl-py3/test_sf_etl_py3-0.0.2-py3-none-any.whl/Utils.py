# -*- coding: utf-8 -*-
import time
import datetime


def get_time(day=0, utc=8.0, time_type='timestamp'):
    """
    :param
        day: 0 当天, 1 第二天, -1 昨天
        utc: 时区, 默认北京时间
        time_type: 返回的数据样式,可选: unix timestamp date
    :return
        字符串
    """
    now_time = int(time.time()) + (day * 86400)  # 当前对应的时间戳
    utc_time = datetime.datetime.utcfromtimestamp(now_time + utc * 3600)
    if time_type == 'unix':
        return str(now_time)
    if time_type == 'date':
        return str(utc_time.strftime("%Y-%m-%d"))
    return str(utc_time.strftime("%Y-%m-%d %H:%M:%S"))

