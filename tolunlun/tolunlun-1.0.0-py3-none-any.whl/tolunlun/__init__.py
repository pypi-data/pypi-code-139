
# -*- coding: utf-8 -*-

import ctypes
import os
import sys

dirname, _ = os.path.split(os.path.abspath(__file__))
lib = ctypes.cdll.LoadLibrary(
    dirname + "/libtolunlun.so")

lib.run.argtypes = None
lib.run.restype = None


def run():
    return lib.run()
