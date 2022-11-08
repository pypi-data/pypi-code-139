from __future__ import annotations

from ..path import rel_to_abs
from .. import yaml_load
import logging
import logging.config
import os
from rich.logging import RichHandler
from pathlib import Path
from ..string.color_string import rgb_string, color_const


def setup_logging(config_path: str | Path = None, multi=False):
    """Setup logging from config file.

    Parameters
    ----------
    config_path : str|Path, default None
        logging config file(.yaml)
    multi : bool
        是否多进程中使用logger

    Examples
    --------
    >>> import logging
    >>> setup_logging()
    >>> logger = logging.getLogger("debug") # Optional: "debug", "info"
    """
    if config_path is None:
        config_path = rel_to_abs("./conf/logging.yaml")
    log_path = Path("./log/")
    if not log_path.exists():
        print(rgb_string(f"Not Found default log path, create dir: `{str(log_path)}`",
                         color=color_const.GOLD))
        log_path.mkdir()
    if os.path.exists(config_path):
        from logging import handlers
        setattr(logging, "RichHandler", RichHandler)
        if multi:
            from concurrent_log_handler import ConcurrentRotatingFileHandler
            setattr(handlers, 'RotatingFileHandler', ConcurrentRotatingFileHandler)
        logging_config = yaml_load(config_path)
        origin_handlers = logging_config['handlers']
        for handler_name in origin_handlers:
            if handler_name.startswith('file'):
                handler_file = origin_handlers[handler_name]['filename']
                abs_handler_file = os.path.join(log_path, handler_file)
                origin_handlers[handler_name]['filename'] = abs_handler_file
        logging.config.dictConfig(logging_config)
        print(rgb_string("Init logging by config success !", color=color_const.GREEN))
    else:
        raise SystemExit(f"logging config file {config_path} not found, exit main processing")
