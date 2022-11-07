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
"""Utils Module"""
from typing import Dict, List, Tuple, Union

from aicc_tools.utils import Const


def check_list(var_name: str, list_var: Union[Tuple, List], num: int):
    """Checks the legitimacy of elements within a node or device list.

    Args:
        var_name (str): The Name of variable need to check.
        list_var (tuple or list): Variables in list format.
        num (int): The number of nodes or devices.

    Returns:
        None
    """
    for value in list_var:
        if value >= num:
            raise ValueError('The index of the {} needs to be less than the number of nodes {}.'.format(var_name, num))


def generate_rank_list(stdout_nodes: Union[List, Tuple], stdout_devices: Union[List, Tuple]):
    """Generate a list of the ranks to output the log.

    Args:
        stdout_nodes (list or tuple): The compute nodes that will
            output the log to stdout.
        stdout_devices (list or tuple): The compute devices that will
            output the log to stdout.

    Returns:
        rank_list (list): A list of the ranks to output the log to stdout.
    """
    rank_list = []
    for node in stdout_nodes:
        for device in stdout_devices:
            rank_list.append(8*node + device)

    return rank_list


def convert_nodes_devices_input(var: Union[List, Tuple, Dict[str, int], None], num: int) -> Union[List, Tuple]:
    """Convert node and device inputs to list format.

    Args:
        var (list[int] or tuple[int] or dict[str, int] or optional):
            The variables that need to be converted to the format.
        num (str): The number of nodes or devices.

    Returns:
        var (list[int] or tuple[int]): A list of nodes or devices.
    """
    if var is None:
        var = tuple(range(num))
    elif isinstance(var, dict):
        var = tuple(range(var['start'], var['end']))

    return var


const = Const()
const.LEVEL = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
const.MODELARTS_LOG_FILE_DIR = '/cache/ma-user-work/'
const.LOCAL_DEFAULT_LOG_FILE_DIR = './log/'
const.RANK_DIR_FORMATTER = 'rank_{}/log/'
const.DEFAULT_FILEHANDLER_FORMAT = '[%(levelname)s] %(asctime)s [%(pathname)s:%(lineno)d] %(funcName)s: %(message)s'
const.DEFAULT_STDOUT_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
const.DEFAULT_REDIRECT_FILE_NAME = 'mindspore.log'
