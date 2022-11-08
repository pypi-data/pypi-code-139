#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
# File: database.py
# Project: Sloppy
# Created Date: 2022-07-25, 09:20:34
# Author: Chungman Kim(h2noda@unipark.kr)
# Last Modified: Tue Sep 06 2022
# Modified By: Chungman Kim
# Copyright (c) 2022 Unipark
# HISTORY:
# Date      	By	Comments
# ----------	---	----------------------------------------------------------
'''

import message
import psycopg2


class Db:
    def __init__(self, type, server, db, port, id, pw):
        self.type = type
        self.server = server
        self.db = db
        self.port = port
        self.id = id
        self.pw = pw
        if self.type == "postgres":
            pass
            # self.connectstring =
        if self.type == "orcale":
            pass


class Postgres(Db):
    def __init__(self, type, server, db, port, id, pw):
        super(Postgres, self).__init__(type, server, db, port, id, pw)
        pass
    
    def generate_connectstring(self):
        pass

class Mysql:
    pass


class Oracle:
    pass
