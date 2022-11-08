#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
# File: common.py
# Project: Sloppy
# Created Date: 2022-07-18, 09:15:59
# Author: Chungman Kim(h2noda@unipark.kr)
# Last Modified: Tue Nov 08 2022
# Modified By: Chungman Kim
# Copyright (c) 2022 Unipark
# HISTORY:
# Date      	By	Comments
# ----------	---	----------------------------------------------------------
'''

from datetime import date, timedelta, datetime
from dateutil.relativedelta import *

from Sloppy.message import *


class Datetime:
    def get_today(strformat="%Y%m%d"):
        """지정된 형식으로 금일 날짜를 리턴

        Args:
            strformat (str, optional): _description_. Defaults to "%Y%m%d".

        Returns:
            _type_: _description_
        """
        retval = date.today().strftime(strformat)

        return retval

    def get_now(strformat="%Y-%m-%d %H:%M:%S"):
        """지정된 형식으로 현재 시간을 리턴

        Args:
            strformat (str, optional): _description_. Defaults to "%Y-%m-%d %H:%M:%S".

        Returns:
            _type_: _description_
        """
        retval = datetime.now().strftime(strformat)

        return retval

    def get_thismonth(strformat="%Y%m"):
        """지정된 형식으로 현재 년월을 리턴

        Args:
            strformat (str, optional): _description_. Defaults to "%Y%m".

        Returns:
            _type_: _description_
        """
        retval = date.today().strftime(strformat)

        return retval

    def get_yesterday(strformat="%Y%m%d"):
        """지정된 형식으로 전일을 리턴

        Args:
            strformat (str, optional): _description_. Defaults to "%Y%m".

        Returns:
            _type_: _description_
        """
        retval = date.today() - timedelta(1)
        retval = retval.strftime(strformat)

        return retval

    def get_previousmonth(strformat="%Y%m"):
        """지정된 형식으로 전월을 리턴

        Args:
            strformat (str, optional): _description_. Defaults to "%Y%m".

        Returns:
            _type_: _description_
        """
        retval = datetime.today() + relativedelta(months=-1)
        retval = retval.strftime(strformat)

        return retval
