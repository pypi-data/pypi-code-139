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
"""Utils."""
import os
from typing import Tuple
from multiprocessing import Process

import numpy as np

from mindspore import Tensor
from mindspore import context
from mindspore.common import set_seed
from mindspore.communication.management import init, get_group_size, get_rank

from aicc_tools.utils.validator import check_in_modelarts, Validator

PARALLEL_MODE = {'DATA_PARALLEL': context.ParallelMode.DATA_PARALLEL,
                 'SEMI_AUTO_PARALLEL': context.ParallelMode.SEMI_AUTO_PARALLEL,
                 'AUTO_PARALLEL': context.ParallelMode.AUTO_PARALLEL,
                 'HYBRID_PARALLEL': context.ParallelMode.HYBRID_PARALLEL,
                 0: context.ParallelMode.DATA_PARALLEL,
                 1: context.ParallelMode.SEMI_AUTO_PARALLEL,
                 2: context.ParallelMode.AUTO_PARALLEL,
                 3: context.ParallelMode.HYBRID_PARALLEL}

MODE = {'PYNATIVE_MODE': context.PYNATIVE_MODE,
        'GRAPH_MODE': context.GRAPH_MODE,
        0: context.GRAPH_MODE,
        1: context.PYNATIVE_MODE}

SAVE_WORK_PATH = '/cache/ma-user-work/rank_{}'
LOCAL_DEFAULT_PATH = './output'
DEBUG_INFO_PATH = '/cache/debug'
PROFILE_INFO_PATH = '/cache/profile'
SLOG_PATH = '/var/log/npu/slog'
PLOG_PATH = '/root/ascend/log/plog'
CONTEXT_CONFIG = {'mode': 'GRAPH_MODE', 'device_target': 'Ascend', 'device_id': 0, 'save_graphs': False}
PARALLEL_CONFIG = {'parallel_mode': 'DATA_PARALLEL', 'gradients_mean': True}


def context_init(seed=0, use_parallel=True, context_config=None, parallel_config=None):
    """Context initialization for MindSpore."""
    Validator.check_type(seed, int)
    Validator.check_type(use_parallel, bool)

    if context_config is None:
        context_config = CONTEXT_CONFIG
    if parallel_config is None:
        parallel_config = PARALLEL_CONFIG

    _set_check_context_config(context_config)
    _set_check_parallel_config(parallel_config)

    np.random.seed(seed)
    set_seed(seed)
    device_num = 1
    rank_id = 0
    context_config['mode'] = MODE.get(context_config.get('mode'))

    if use_parallel:
        init()
        device_id = int(os.getenv('DEVICE_ID', 0))  # 0 ~ 7
        rank_id = get_rank()  # local_rank
        device_num = get_group_size()  # world_size
        context_config['device_id'] = device_id
        parallel_config['parallel_mode'] = PARALLEL_MODE.get(parallel_config.get('parallel_mode'))
        context.set_context(**context_config)
        context.reset_auto_parallel_context()
        context.set_auto_parallel_context(
            device_num=device_num, **parallel_config)
    else:
        context.set_context(**context_config)
    return rank_id, device_num


def _set_check_context_config(config):
    """Set context config."""
    mode = config.get('mode')
    if mode is None:
        config.setdefault('mode', 0)
    if mode not in MODE.keys():
        raise IndexError('Running mode should be in {}, but get {}'.format(MODE.keys(), mode))

    device = config.get('device_id')
    if device is None:
        config.setdefault('device_id', 0)

    if check_in_modelarts():
        save_graph = config.get('save_graphs')
        if save_graph:
            save_graphs_path = config.get('save_graphs_path')
            if save_graphs_path is None:
                config.setdefault('save_graphs_path', save_graphs_path)
                save_graphs_path = os.path.join(DEBUG_INFO_PATH, 'graphs_info')
                config['save_graphs_path'] = save_graphs_path
        enable_dump = config.get('enable_dump')
        if enable_dump:
            save_dump_path = config.get('save_dump_path')
            if save_dump_path is None:
                config.setdefault('save_dump_path', save_dump_path)
                save_dump_path = os.path.join(DEBUG_INFO_PATH, 'dump_info')
                config.setdefault('save_dump_path', save_dump_path)


def _set_check_parallel_config(config):
    """Set parallel config."""
    parallel_mode = config.get('parallel_mode')
    if parallel_mode is None:
        config.setdefault('parallel_mode', 0)

    if parallel_mode not in PARALLEL_MODE.keys():
        raise IndexError(
            'Running parallel mode should be in {}, but get {}'.format(PARALLEL_MODE.keys(), parallel_mode))


def sync_trans(f):
    """Asynchronous transport decorator."""
    try:
        def wrapper(*args, **kwargs):
            pro = Process(target=f, args=args, kwargs=kwargs)
            pro.start()
            return pro
        return wrapper
    except Exception as e:
        raise e


def get_net_outputs(params):
    """Get network outputs."""
    if isinstance(params, (tuple, list)):
        if isinstance(params[0], Tensor) and isinstance(params[0].asnumpy(), np.ndarray):
            params = params[0]
    elif isinstance(params, Tensor) and isinstance(params.asnumpy(), np.ndarray):
        params = np.mean(params.asnumpy())
    return params


def get_rank_info() -> Tuple[int, int]:
    """Get rank_info from environment variables.

    Returns:
        rank_id (int): Rank id.
        rand_size (int): The number of rank.
    """
    rank_id = int(os.getenv('RANK_ID', '0'))
    rank_size = int(os.getenv('RANK_SIZE', '1'))

    return rank_id, rank_size


def get_num_nodes_devices(rank_size: int) -> Tuple[int, int]:
    """Derive the number of nodes and devices based on rank_size.

    Args:
        rank_size (int): rank size.

    Returns:
       num_nodes (int): number of nodes.
       num_devices (int): number of devices.
    """
    if rank_size in (2, 4, 8):
        num_nodes = 1
        num_devices = rank_size
    else:
        num_nodes = rank_size // 8
        num_devices = 8

    return num_nodes, num_devices


class Const:

    def __setattr__(self, key, value):
        if key in self.__dict__:
            raise PermissionError('Can not change const {0}.'.format(key))
        if not key.isupper():
            raise ValueError('Const name {0} is not all uppercase.'.format(key))
        self.__dict__[key] = value
