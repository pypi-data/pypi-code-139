# -*- coding: UTF-8 -*-

class InfoManClass:

    def __init__(self):
        pass

    @staticmethod
    def INFO_ERR(info):
        print("\033[0;31m" + info + "\033[0m")

    @staticmethod
    def INFO_NOTE(info):
        print("\033[0;36m" + info + "\033[0m")

    @staticmethod
    def INFO_SUCC(info):
        print("\033[0;32m" + info + "\033[0m")