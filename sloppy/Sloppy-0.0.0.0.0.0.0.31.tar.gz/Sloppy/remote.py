#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
# File: remote.py
# Project: Sloppy
# Created Date: 2022-07-18, 09:19:06
# Author: Chungman Kim(h2noda@unipark.kr)
# Last Modified: Thu Sep 01 2022
# Modified By: Chungman Kim
# Copyright (c) 2022 Unipark
# HISTORY:
# Date      	By	Comments
# ----------	---	----------------------------------------------------------
'''
from message import *
from error import *
import paramiko


class Remote:
    def ssh_command(p_id, p_pw, p_remote, p_cmd):
        """Excute - SSH Command 

        Args:
            p_id (String): User id
            p_pw (String): User Password
            p_remote (String): Remoter Server Hostname OR IP
            p_cmd (String): Command
        """
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            ssh.connect(hostname=p_remote, port=22,
                        username=p_id, password=p_pw)

            Msg.printmsg("Connected Remote Server(ID : " +
                         p_id, 1, "-", "red", True)

            (stdin, stdout, stderr) = ssh.exec_command(p_cmd)
            #output = stdout.readlines()

        except Exception as err:
            print(err)
        finally:
            ssh.close()
