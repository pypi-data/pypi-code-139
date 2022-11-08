# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/8/25 10:28
# @Author  : lgq
# @Site    :
# @File    : format
# @Software: PyCharm

import os
import logging
from logging.handlers import RotatingFileHandler
from logging.handlers import SysLogHandler
from logging.handlers import TimedRotatingFileHandler
from .colors import Fore as ForegroundColors
from .format import LogFormatter, JsonFormatter

try:
    import curses  # type: ignore
except ImportError:
    curses = None

# logten default logger
logger = None  # pylint: disable=invalid-name

_loglevel = logging.DEBUG  # pylint: disable=invalid-name
_logfile = None  # pylint: disable=invalid-name
_formatter = None  # pylint: disable=invalid-name

DEFAULT_LOGGER = "logten_default"
INTERNAL_LOGGER_ATTR = "_is_logten_internal"
HANDLER_IS_CUSTOM_LOGLEVEL = "_is_logten_loglevel"

# setup colorama on Windows
if os.name == 'nt':
    from colorama import init as colorama_init

    colorama_init()


def setup_logger(name=None, logfile=None, level=logging.DEBUG, formatter=None, file_log_level=None):
    '''
    初始化 logger
    :param name: logger name
    :param logfile: 存储 log 到文件
    :param level: 控制台 log 的级别
    :param formatter: log 的输出格式，支持自定义
    :param file_log_level: 文件 log 的级别
    :return: logger 对象
    '''
    _logger = logging.getLogger(name or __name__)
    _logger.propagate = False
    _logger.setLevel(level)

    # Reconfigure existing handlers
    stderr_stream_handler = None
    for handler in list(_logger.handlers):
        if hasattr(handler, INTERNAL_LOGGER_ATTR):
            if isinstance(handler, logging.FileHandler):
                # Internal FileHandler needs to be removed and re-setup to be able
                # to set a new logfile.
                _logger.removeHandler(handler)
                continue
            elif isinstance(handler, logging.StreamHandler):
                stderr_stream_handler = handler

        # reconfigure handler
        handler.setLevel(level)
        handler.setFormatter(formatter or LogFormatter())

    if stderr_stream_handler is None:
        stderr_stream_handler = logging.StreamHandler()
    setattr(stderr_stream_handler, INTERNAL_LOGGER_ATTR, True)
    stderr_stream_handler.setLevel(level)
    stderr_stream_handler.setFormatter(formatter or LogFormatter())
    _logger.addHandler(stderr_stream_handler)

    if logfile:
        filehandler = TimedRotatingFileHandler(filename=logfile)
        setattr(filehandler, INTERNAL_LOGGER_ATTR, True)
        filehandler.setLevel(file_log_level or level)
        filehandler.setFormatter(formatter or LogFormatter(color=False))
        _logger.addHandler(filehandler)

    return _logger


def setup_default_logger(logfile=None, level=logging.DEBUG, formatter=None):
    global logger  # pylint: disable=invalid-name
    logger = setup_logger(name=DEFAULT_LOGGER, logfile=logfile, level=level, formatter=formatter)
    return logger


def reset_default_logger():
    global logger  # pylint: disable=invalid-name
    global _loglevel  # pylint: disable=invalid-name
    global _logfile  # pylint: disable=invalid-name
    global _formatter  # pylint: disable=invalid-name
    _loglevel = logging.DEBUG
    _logfile = None
    _formatter = None
    logger = setup_logger(name=DEFAULT_LOGGER, logfile=_logfile, level=_loglevel, formatter=_formatter)
    return logger


reset_default_logger()


def __remove_internal_loggers(logger_to_update, disable_stderr=True):
    for handler in list(logger_to_update.handlers):
        if hasattr(handler, INTERNAL_LOGGER_ATTR):
            if isinstance(handler, RotatingFileHandler):
                logger_to_update.removeHandler(handler)
            elif isinstance(handler, SysLogHandler):
                logger_to_update.removeHandler(handler)
            elif isinstance(handler, logging.StreamHandler) and disable_stderr:
                logger_to_update.removeHandler(handler)


def logfile(filename, formatter=None, encoding=None, loglevel=None, when='h'):
    '''
    定义输出log到文件
    :param filename: log 文件的名称
    :param formatter:  定义输出 log 的格式，支持自定义
    :param encoding:  输出编码格式，默认 utf-8
    :param loglevel:  文件 log 的级别
    :param when: 文件写入支持按照时间分桶，这里是多久进行一次分桶
    :return:
    '''
    if filename:
        filehandler = TimedRotatingFileHandler(filename, when=when, encoding=encoding)

        setattr(filehandler, INTERNAL_LOGGER_ATTR, True)
        filehandler.setLevel(loglevel or _loglevel)
        filehandler.setFormatter(formatter or _formatter or LogFormatter(color=True))
        logger.addHandler(filehandler)


if __name__ == '__main__':
    _logger = reset_default_logger()
    _logger.info('test')
