#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CRC:0:0
# Функции, классы для работы с датами (временем)

from datetime import datetime, date as datetype, timedelta
from dataclasses import dataclass
from typing import Union

DateParam = Union[datetime | datetype] | None


@dataclass
class DateRange:
    date_beg: DateParam
    date_end: DateParam


def _date_to_datetime(date) -> datetime:
    if date:
        s = date.isoformat()
        if type(date) is datetype:
            return datetime.fromisoformat(s + " 00:00:00+00:00")
        elif "+" not in s:  # добавляем timezone
            return datetime.fromisoformat(date.isoformat() + "+00:00")
    return date


def date_range(date_beg: DateParam = None,
               date_end: DateParam = None) -> DateRange:
    return DateRange(
        date_beg=_date_to_datetime(date_beg or datetime.min),
        date_end=_date_to_datetime(date_end or datetime.max))


def offset_date(date: DateParam, n: int) -> datetime:
    return _date_to_datetime(date) + timedelta(days=n)


def now() -> datetime:
    return _date_to_datetime(datetime.now())


def today() -> datetime:
    return _date_to_datetime(datetime.now().date())


def datetime_norm(date: DateParam = None) -> datetime:
    return _date_to_datetime(date) if date else now()


def date_norm(date: DateParam = None) -> datetime:
    _d = date.date() if type(date) is datetime else date
    return _date_to_datetime(_d) if date else today()
