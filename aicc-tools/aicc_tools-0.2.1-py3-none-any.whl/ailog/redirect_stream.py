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
"""Redirect Stream"""
import os
import stat
import sys
from functools import wraps
from tempfile import TemporaryFile
from typing import Dict, List, Tuple, Union

from aicc_tools.ailog.ailog_utils import check_list, const, convert_nodes_devices_input, generate_rank_list
from aicc_tools.utils import check_in_modelarts, get_num_nodes_devices, get_rank_info


def judge_redirect(rank_id: int,
                   rank_size: int,
                   redirect_nodes: Union[List, Tuple, Dict[str, int], None] = None,
                   redirect_devices: Union[List, Tuple, Dict[str, int], None] = None):
    """Determine if the stderr of this process needs to be redirected.

    Args:
        rank_id (int): Rank id.
        rank_size (int): Rank Size.
        redirect_nodes (list or tuple or dict or None): Node list. The
            nodes in the list will redirect stderr.
        redirect_devices (list or tuple or dict or None): Device
            list. The devices in the list will redirect stderr.

    Returns:
        prerequisite (bool): If true, stderr will redirect.
    """
    is_redirect = True
    if rank_size > 1 and (redirect_nodes is not None or redirect_devices is not None):
        num_nodes, num_devices = get_num_nodes_devices(rank_size)
        redirect_nodes = convert_nodes_devices_input(redirect_nodes, num_nodes)
        redirect_devices = convert_nodes_devices_input(redirect_devices, num_devices)
        check_list('nodes', redirect_nodes, num_nodes)
        check_list('devices', redirect_devices, num_devices)
        rank_list = generate_rank_list(redirect_nodes, redirect_devices)
        if rank_id not in rank_list:
            is_redirect = False

    return is_redirect


class StreamRedirector:

    def __init__(self, source_stream, target_stream):
        """Redirects the source stream to the target stream.

        Args:
            source_stream: Source stream.
            target_stream: Target stream.
        """
        super(StreamRedirector, self).__init__()

        self.source_stream = source_stream
        self.target_stream = target_stream

        self.save_source_stream_fd = os.dup(self.source_stream.fileno())

    def __call__(self, func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            self.start()
            func(*args, **kwargs)
            self.stop()

        return wrapper

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def start(self):
        self.source_stream.flush()
        os.dup2(self.target_stream.fileno(), self.source_stream.fileno())

    def stop(self):
        self.source_stream.flush()
        os.dup2(self.save_source_stream_fd, self.source_stream.fileno())
        self.target_stream.flush()


class AiLogFastStreamRedirect2File(StreamRedirector):

    def __init__(self,
                 source_stream=None,
                 redirect_nodes: Union[List, Tuple, Dict[str, int], None] = None,
                 redirect_devices: Union[List, Tuple, Dict[str, int], None] = None,
                 **kwargs):
        """Redirect stream to file.

        Args:
            source_stream (file object or None): Streams that need to be redirected.
                Default: None, select stderr.
            redirect_nodes (list[int] or tuple[int] or optional): The computation
                nodes that will redirect stderr.
                Default is None: indicates that all nodes will redirect stderr.
                Eg [0, 1, 2, 3] or (0, 1, 2, 3): indicates that nodes 0, 1, 2,
                    and 3 all redirect stderr.
            redirect_devices (list[int] or tuple[int] or optional): The computation
                devices that will redirect stderr.
                Default is None, indicates that all devices will redirect stderr.
                Eg [0, 1, 2, 3] or (0, 1, 2, 3): indicates that devices 0, 1, 2,
                    and 3 all redirect stderr.
            kwargs (dict): File-related parameters.
                file_save_dir (str): The folder where the files that
                    save redirected stream are saved.
                append_rank_dir (bool): Whether to add a folder with the format rank{}.
                file_name (str): Redirect file name.
        """
        rank_id, rank_size = get_rank_info()

        self.is_redirect = judge_redirect(rank_id=rank_id,
                                          rank_size=rank_size,
                                          redirect_nodes=redirect_nodes,
                                          redirect_devices=redirect_devices)

        file_save_dir = kwargs.get('file_save_dir', '')
        append_rank_dir = kwargs.get('append_rank_dir', True)
        file_name = kwargs.get('file_name', '')

        if not file_save_dir:
            file_save_dir = const.LOCAL_DEFAULT_LOG_FILE_DIR
        if check_in_modelarts():
            file_save_dir = const.MODELARTS_LOG_FILE_DIR
        if append_rank_dir:
            rank_str = const.RANK_DIR_FORMATTER.format(rank_id)
            file_save_dir = os.path.join(file_save_dir, rank_str)

        if not file_name:
            file_name = const.DEFAULT_REDIRECT_FILE_NAME
        self.file_path = os.path.join(file_save_dir, file_name)
        self.file_save_dir = os.path.dirname(self.file_path)

        if source_stream is None:
            source_stream = sys.stderr
        target_stream = TemporaryFile(mode='w+')

        super(AiLogFastStreamRedirect2File, self).__init__(source_stream=source_stream, target_stream=target_stream)

    def start(self):
        if self.is_redirect:
            super(AiLogFastStreamRedirect2File, self).start()

    def stop(self):
        if self.is_redirect:
            self.target_stream.flush()
            if not os.path.exists(self.file_save_dir):
                os.makedirs(self.file_save_dir)
            self.target_stream.seek(0, 0)
            flags = os.O_WRONLY | os.O_CREAT
            modes = stat.S_IWUSR | stat.S_IRUSR
            with os.fdopen(os.open(self.file_path, flags, modes), 'w') as f:
                for line in self.target_stream:
                    f.write(line)
            super(AiLogFastStreamRedirect2File, self).stop()
            self.target_stream.close()
