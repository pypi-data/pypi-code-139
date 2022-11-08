#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
# File: message.py
# Project: Sloppy
# Created Date: 2022-07-18, 09:18:14
# Author: Chungman Kim(h2noda@unipark.kr)
# Last Modified: Tue Nov 08 2022
# Modified By: Chungman Kim
# Copyright (c) 2022 Unipark
# HISTORY:
# Date      	By	Comments
# ----------	---	----------------------------------------------------------
'''

from rich.console import Console
from rich.table import Table


class Msg:
    def __init__(self):
        self.cs = Console()
        self.table = Table()

    def blank(self):
        self.cs.print()

    def copyright(self):
        self.printmsg(
            "Copyright 2022. Unipark. All right reserved.", color="yellow", bold=True)

    def OK(self, indent_char="-", indent=0):
        print_txt = self.prefix(indent_char, indent) + \
            "[" + self.style_tag("dark_orange", False) + \
            "]OK" + "[/" + self.style_tag("dark_orange", False) + "]"
        self.printmsg(print_txt, color="white")

    def prefix(self, indent_char="-", indent=0):
        if indent == 0:
            retval = ""
        else:
            retval = "  " * indent + indent_char + " "
        return retval

    def style_tag(self, color, bold=False):
        if bold == False:
            retval = color
        else:
            retval = "bold " + color
        return retval

    def repeat_char(self, char="#", repeat=35, color="green"):
        retval = char * repeat
        self.printmsg(retval, "", 0, color, True)

    def printmsg(self, val, indent_char="-", indent=0, color="white", bold=False, end="\n"):
        retstyle = self.style_tag(color, bold)
        retval = self.prefix(indent_char, indent) + \
            "[" + retstyle + "]" + val + "[/" + retstyle + "]"

        self.cs.print(retval, style="white")

    def title(self, val, color="green"):
        lenval = len(val)
        self.blank()
        self.repeat_char("#", lenval + 6, color)
        self.printmsg("#  " + " " * lenval + "  #", "", 0, color, True)
        self.printmsg("#  " + val + "  #", "", 0, color, True)
        self.printmsg("#  " + " " * lenval + "  #", "", 0, color, True)
        self.repeat_char("#", lenval + 6, color)
        self.blank()

    def input(self, val, indent=0, indent_char="-", color="white", bold=False):
        styletag = self.style_tag(color, bold)
        strinput = self.prefix(indent_char, indent) + \
            "[" + styletag + "]" + val + "[/" + styletag + "]"
        return self.cs.input(strinput)

    def input_passwd(self, val, indent=0, indent_char="-", color="white", bold=False):
        strprefix = self.prefix(indent, indent_char)
        styletag = self.style_tag(color, bold)
        strinput = strprefix + "[" + styletag + "]" + \
            val + "[/" + styletag + "]"
        return self.cs.input(strinput, password=True)

    def gen_table(self, p_coldata, p_rowdata):
        for i in range(len(p_coldata)):
            self.table.add_column(p_coldata[i])

        for row in p_rowdata:
            self.table.add_row(row[0], row[1], row[2], str(row[3]))
        Console.print(self.table)
