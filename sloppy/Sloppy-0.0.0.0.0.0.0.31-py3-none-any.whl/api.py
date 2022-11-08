#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
# File: web.py
# Project: Sloppy
# Created Date: 2022-09-27, 07:49:41
# Author: Chungman Kim(h2noda@unipark.kr)
# Last Modified: Tue Sep 27 2022
# Modified By: Chungman Kim
# Copyright (c) 2022 Unipark
# HISTORY:
# Date      	By	Comments
# ----------	---	----------------------------------------------------------
'''

from http.client import HTTPSConnection
from base64 import b64encode
import ssl

# Local Package
from Sloppy.message import *


class Api:
    def __init__(self, userid, userpw, server, port):
        self.userid = userid
        self.userpw = userpw
        self.server = server
        self.port = port

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        self._key = key

    # def credentials(userid, userpw)
