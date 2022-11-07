# Copyright 2022 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""LOG Module"""
import logging
import logging.config
import logging.handlers
import os
import sys
from typing import Dict, List, Tuple, Union

from aicc_tools.ailog.ailog_utils import check_list, const, convert_nodes_devices_input, generate_rank_list
from aicc_tools.utils import check_in_modelarts, get_num_nodes_devices, get_rank_info

logger_list = []


def judge_stdout(rank_id: int,
                 rank_size: int,
                 is_output: bool,
                 nodes: Union[List, Tuple, Dict[str, int], None] = None,
                 devices: Union[List, Tuple, Dict[str, int], None] = None) -> bool:
    """Determines if logs will be output.

    Args:
        rank_id (int): Rank id.
        rank_size (int): Rank size.
        is_output (int): If set to true, logs or others will be output.
        nodes (list or tuple or dict or None): Node list. The nodes in the list
            will output the log to stdout.
        devices (list or tuple or dict or None): Device list. The devices
            in the list or output the log to stdout.

    Returns:
        is_output (bool): If set to true, logs or others will be output
            or redirect.
    """
    if is_output and rank_size > 1 and (nodes is not None or devices is not None):
        num_nodes, num_devices = get_num_nodes_devices(rank_size)
        stdout_nodes = convert_nodes_devices_input(nodes, num_nodes)
        stdout_devices = convert_nodes_devices_input(devices, num_devices)
        check_list('nodes', stdout_nodes, num_nodes)
        check_list('devices', stdout_devices, num_devices)
        rank_list = generate_rank_list(stdout_nodes, stdout_devices)
        if rank_id not in rank_list:
            is_output = False

    return is_output


def validate_nodes_devices_input(var_name: str, var):
    """Check the list of nodes or devices.

    Args:
        var_name (str): Variable name.
        var: The name of the variable to be checked.

    Returns:
        None
    """
    if not (var is None or isinstance(var, (list, tuple, dict))):
        raise TypeError('The value of {} can be None or a value of type tuple, ' 'list, or dict.'.format(var_name))
    if isinstance(var, (list, tuple)):
        for item in var:
            if not isinstance(item, int):
                raise TypeError('The elements of a variable of type list or ' 'tuple must be of type int.')


def validate_level(var_name: str, var):
    """Verify that the log level is correct.

    Args:
        var_name (str): Variable name.
        var: The name of variable to be checked.

    Returns:
        None
    """
    if not isinstance(var, str):
        raise TypeError('The format of {} must be of type str.'.format(var_name))
    if var not in const.LEVEL:
        raise ValueError('{}={} needs to be in {}'.format(var_name, var, const.LEVEL))


def validate_std_input_format(to_std: bool, stdout_nodes: Union[List, Tuple, None],
                              stdout_devices: Union[List, Tuple, None], stdout_level: str):
    """Validate the input about stdout of the get_logger function."""

    if not isinstance(to_std, bool):
        raise TypeError('The format of the to_std must be of type bool.')

    validate_nodes_devices_input('stdout_nodes', stdout_nodes)
    validate_nodes_devices_input('stdout_devices', stdout_devices)
    validate_level('stdout_level', stdout_level)


def validate_file_input_format(file_level: Union[List[str], Tuple[str]], file_save_dir: str, append_rank_dir: str,
                               file_name: Union[List[str], Tuple[str]]):
    """Validate the input about file of the get_logger function."""

    if not (isinstance(file_level, tuple) or isinstance(file_level, list)):
        raise TypeError('The value of file_level should be list or a tuple.')
    for level in file_level:
        validate_level('level in file_level', level)

    if not len(file_level) == len(file_name):
        raise ValueError('The length of file_level and file_name should be equal.')

    if not isinstance(file_save_dir, str):
        raise TypeError('The value of file_save_dir should be a value of type str.')

    if not isinstance(append_rank_dir, bool):
        raise TypeError('The value of append_rank_dir should be a value of type bool.')

    if not (isinstance(file_name, tuple) or isinstance(file_name, list)):
        raise TypeError('The value of file_name should be list or a tuple.')
    for name in file_name:
        if not isinstance(name, str):
            raise TypeError('The value of name in file_name should be a value of type str.')


def _convert_level(level: str) -> int:
    """Convert the format of the log to logging level.

    Args:
        level (str): User log level.

    Returns:
        level (str): Logging level.
    """
    level_convert = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    level = level_convert.get(level, logging.INFO)

    return level


def get_logger(logger_name: str = 'aicc', **kwargs) -> logging.Logger:
    """Get the logger. Both computing centers and bare metal servers are
    available.

    Args:
        logger_name (str): Logger name.
        kwargs (dict): Other input.
            to_std (bool): If set to True, output the log to stdout.
            stdout_nodes (list[int] or tuple[int] or optional):
                The computation nodes that will output the log to stdout.
                default: None, indicates that all nodes will output logs to stdout.
                eg: [0, 1, 2, 3] or (0, 1, 2, 3): indicates that nodes 0, 1, 2, and
                    3 all output logs to stdout.
            stdout_devices (list[int] or tuple[int] or optional):
                The computation devices that will output the log to stdout.
                default: None, indicates that all devices will output logs to stdout.
                eg: [0, 1, 2, 3] or (0, 1, 2, 3): indicates that devices 0, 1, 2,
                    and 3 all output logs to stdout.
            stdout_level (str): The level of the log output to stdout.
                If the type is str, the options are DEBUG, INFO, WARNING, ERROR, CRITICAL.
            stdout_format (str): Log format.
            file_level (list[str] or tuple[str]): The level of the log output to file.
                eg: ['INFO', 'ERROR'] Indicates that the logger will output logs above
                    the level INFO and ERROR in the list to the corresponding file.
                The length of the list needs to be the same as the length of file_name.
            file_save_dir (str): The folder where the log files are stored.
            append_rank_dir (bool): Whether to add a folder with the format rank{}.
            file_name (list[str] or list[tuple]): Store a list of output file names.
            max_file_size (int): The maximum size of a single log file. Unit: MB.
            max_num_of_files (int): The maximum number of files to save.

    Returns:
        logger (logging.Logger): Logger.
    """
    logger = logging.getLogger(logger_name)
    if logger_name in logger_list:
        return logger

    to_std = kwargs.get('to_std', True)
    stdout_nodes = kwargs.get('stdout_nodes', None)
    stdout_devices = kwargs.get('stdout_devices', (0, ))
    stdout_level = kwargs.get('stdout_level', 'INFO')
    stdout_format = kwargs.get('stdout_format', '')
    file_level = kwargs.get('file_level', ('INFO', 'ERROR'))
    file_save_dir = kwargs.get('file_save_dir', '')
    append_rank_dir = kwargs.get('append_rank_dir', True)
    file_name = kwargs.get('file_name', ('aicc.log', 'error.log'))
    max_file_size = kwargs.get('max_file_size', 50)
    max_num_of_files = kwargs.get('max_num_of_files', 5)

    validate_std_input_format(to_std, stdout_nodes, stdout_devices, stdout_level)
    validate_file_input_format(file_level, file_save_dir, append_rank_dir, file_name)

    rank_id, rank_size = get_rank_info()

    to_std = judge_stdout(rank_id=rank_id,
                          rank_size=rank_size,
                          is_output=to_std,
                          nodes=stdout_nodes,
                          devices=stdout_devices)
    if to_std:
        if not stdout_format:
            stdout_format = const.DEFAULT_STDOUT_FORMAT
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(_convert_level(stdout_level))
        stream_formatter = logging.Formatter(stdout_format)
        stream_handler.setFormatter(stream_formatter)
        logger.addHandler(stream_handler)

    logging_level = []
    for level in file_level:
        logging_level.append(_convert_level(level))

    if not file_save_dir:
        file_save_dir = const.LOCAL_DEFAULT_LOG_FILE_DIR
    if check_in_modelarts():
        file_save_dir = const.MODELARTS_LOG_FILE_DIR
    if append_rank_dir:
        rank_str = const.RANK_DIR_FORMATTER.format(rank_id)
        file_save_dir = os.path.join(file_save_dir, rank_str)

    file_path = []
    for name in file_name:
        path = os.path.join(file_save_dir, name)
        path = os.path.realpath(path)
        base_dir = os.path.dirname(path)
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        file_path.append(path)

    max_file_size = max_file_size * 1024 * 1024

    file_formatter = logging.Formatter(const.DEFAULT_FILEHANDLER_FORMAT)
    for i, level in enumerate(file_level):
        file_handler = logging.handlers.RotatingFileHandler(filename=file_path[i],
                                                            maxBytes=max_file_size,
                                                            backupCount=max_num_of_files)
        file_handler.setLevel(level)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    logger.setLevel(_convert_level('DEBUG'))

    logger_list.append(logger_name)

    return logger
