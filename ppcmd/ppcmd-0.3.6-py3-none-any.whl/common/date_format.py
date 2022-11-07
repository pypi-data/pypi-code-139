import datetime


# YYYY-MM-DD_HHMMSS
def cur_time_str():
    now = datetime.datetime.now()
    return str(now)[0:19].replace(' ', '_').replace(':', '')


# YYMMDD_HHMMSS
def cur_short_time_str():
    now = datetime.datetime.now()
    return str(now)[2:19].replace(' ', '_').replace(':', '').replace('-', '')
