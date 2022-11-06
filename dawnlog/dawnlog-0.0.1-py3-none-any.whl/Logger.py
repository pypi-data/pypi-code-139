# -*- coding:  utf-8 -*-
# @Author:     YLM
# @Time:       2021/4/28 21:50
# @Software:   PyCharm
# @File:       Logger.py


import logging, colorlog
import time
import os


class Log(object):
    __instance = None
    __first_init = True

    def __new__(cls,  *args, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)

        return cls.__instance

    def __init__(self, log_path):

        self.__first_init = False

        self.log_path = log_path

        self.log_colors_config = {
            'DEBUG': 'white',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }

        if not os.path.exists(self.log_path):
            os.mkdir(self.log_path)

        self.log_name = os.path.join(self.log_path, '%s.log' % time.strftime('%Y-%m-%d %H-%M-%S'))
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        # log format
        self.formatter = logging.Formatter(
            fmt='[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s',
            datefmt='%Y-%m-%d  %H:%M:%S'
        )

        # color log format
        self.console_formatter = colorlog.ColoredFormatter(
            fmt='%(log_color)s[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s',
            datefmt='%Y-%m-%d  %H:%M:%S',
            log_colors=self.log_colors_config
        )

    def console(self, level, message):

        # StreamHandler in local
        fh = logging.FileHandler(self.log_name, 'a', encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

        # StreamHandler in console
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.console_formatter)
        self.logger.addHandler(ch)

        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)

        # avoid repetition
        self.logger.removeHandler(ch)
        self.logger.removeHandler(fh)

        fh.close()

    def debug(self, message):
        self.console('debug', message)

    def info(self, message):
        self.console('info', message)

    def warning(self, message):
        self.console('warning', message)

    def error(self, message):
        self.console('error', message)

    def step(self, message):
        self.console('info', "\n\n******************{}********************".format(message))

    def __str__(self):
        return self.log_name


if __name__ == '__main__':
    cur_path = os.path.dirname(os.path.realpath(__file__))
    log_path = os.path.join(cur_path, "logs")
    print(log_path)
