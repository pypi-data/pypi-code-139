#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
# File: datetime.py
# Project: Sloppy
# Created Date: 2022-08-08, 11:02:18
# Author: Chungman Kim(h2noda@unipark.kr)
# Last Modified: Mon Aug 08 2022
# Modified By: Chungman Kim
# Copyright (c) 2022 Unipark
# HISTORY:
# Date      	By	Comments
# ----------	---	----------------------------------------------------------
'''
from datetime import date, timedelta, datetime
from dateutil.relativedelta import *


def get_today():
    retval = date.today().strftime("%Y%m%d")

    return retval


def get_thismonth():
    retval = date.today().strftime("%Y%m")

    return retval


def get_yesterday():
    retval = date.today() - timedelta(1)
    retval = retval.strftime("%Y%m")

    return retval


def get_previousmonth():
    retval = datetime.today() + relativedelta(months=-1)
    retval = retval.strftime("%Y%m")

    return retval
