#!/usr/bin/env python3.6
from dg_query_analysis.utils.langconv import Converter
import hashlib


def md5_encode(key):
    if not isinstance(key, bytes):
        key = key.encode("utf8")
    m2 = hashlib.md5(key)
    return m2.hexdigest()


traditional_to_simplified = Converter('zh-hans')
