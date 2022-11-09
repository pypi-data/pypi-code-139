import os
import sys
import logging
import inspect

class Logger():
    """
    Logging handler, provides simple access to logging levels on a per-module basis:

    DEBUG | INFO | WARNING | ERROR | CRITICAL

    Example usage:

    > from aiaa.utils.logging import Logger

    > Logger.log_debug('Some debug message')

    > Logger.log_critical('Some critical message')
    """

    def __init__(self):
        pass

    @classmethod
    def _log(cls, message, level):
        
        # Fetch the named logger (or create if it doesn't exist) and set severity
        module_name = inspect.stack()[1]
        logger = logging.getLogger(module_name)
        logger.setLevel(level)

        # Ensure all relevant handlers are added to the logger
        cls._ensure_handler_sysout(logger)

        # Initiate logging
        if level == logging.DEBUG:
            logger.debug(message)
        elif level == logging.INFO:
            logger.info(message)
        elif level == logging.WARNING:
            logger.warning(message)
        elif level == logging.ERROR:
            logger.error(message)
        elif level == logging.CRITICAL:
            logger.critical(message)
        else:
            raise ValueError('Logger: Inappropriate level provided: "{}"'.format(level))

    @classmethod
    def log_debug(cls, message):
        cls._log(message, logging.DEBUG)

    @classmethod
    def log_info(cls, message):
        cls._log(message, logging.INFO)

    @classmethod
    def log_warning(cls, message):
        cls._log(message, logging.WARNING)

    @classmethod
    def log_error(cls, message):
        cls._log(message, logging.ERROR)

    @classmethod
    def log_critical(cls, message):
        cls._log(message, logging.CRITICAL)

    @staticmethod
    def _get_formatter():
        return logging.Formatter('%(asctime)s - %(levelname)s - %(name)s.%(funcName)s: %(message)s')

    @classmethod
    def _ensure_handler_sysout(cls, logger: logging.Logger):
        """Ensures that the 'stream-sysout' is attached to the logger."""

        key = 'stream-sysout'

        # Add the handler if it doesn't already exist on the logger
        bools = list(map(lambda h: getattr(h, 'tag', False) == key, logger.handlers))
        if True not in bools:
            
            handler = logging.StreamHandler(stream=sys.stdout)
            handler.setFormatter(cls._get_formatter())
            handler.tag = key
            logger.addHandler(handler)
        