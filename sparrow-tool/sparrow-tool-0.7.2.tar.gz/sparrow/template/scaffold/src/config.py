import os
from sparrow import rel_to_abs, yaml_load
from dynaconf import Dynaconf
from typing import List, Dict
from dataclasses import dataclass
import logging
import logging.config
import yaml



def setup_logging(safety=False):
    config_path = rel_to_abs("conf/logging.yaml")
    log_path = rel_to_abs("log/")
    if not os.path.exists(log_path):
        print(f"Not Found default log path, create {log_path}")
        os.makedirs(log_path)
    if os.path.exists(config_path):
        if safety:
            from utilities.safe_logging import SafeRotatingFileHandler, SafeTimedRotatingFileHandler
            from logging import handlers
            setattr(handlers, 'SafeRotatingFileHandler', SafeRotatingFileHandler)
            setattr(handlers, 'SafeTimedRotatingFileHandler', SafeTimedRotatingFileHandler)
        logging_config = yaml_load(config_path)
        origin_handlers = logging_config['handlers']
        for handler_name in origin_handlers:
            if handler_name.startswith('file'):
                handler_file = origin_handlers[handler_name]['filename']
                abs_handler_file = os.path.join(log_path, handler_file)
                origin_handlers[handler_name]['filename'] = abs_handler_file
        logging.config.dictConfig(logging_config)
        print("Init logging by config success !")
    else:
        raise SystemExit(f"logging config file {config_path} not found, exit main processing")


setup_logging(True)
# logger = logging.getLogger("project_dummy")
