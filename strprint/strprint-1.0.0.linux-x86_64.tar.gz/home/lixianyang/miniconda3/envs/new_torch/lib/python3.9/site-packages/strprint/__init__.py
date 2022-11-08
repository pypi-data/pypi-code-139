
# -*- coding: utf-8 -*-

import ctypes
import os
import sys

dirname, _ = os.path.split(os.path.abspath(__file__))
lib = ctypes.cdll.LoadLibrary(
    dirname + "/libstr_print_c_warpper.so")

lib.str_print.argtypes = [ctypes.c_char_p]
lib.str_print.restype = ctypes.c_char_p


def str_print(text):
    return lib.str_print(text)
