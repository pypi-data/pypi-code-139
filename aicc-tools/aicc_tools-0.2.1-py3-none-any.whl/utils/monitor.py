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
"""Monitor."""
import time
import logging as logger

import numpy as np

from mindspore.profiler import Profiler
from mindspore.train.callback import Callback, ModelCheckpoint, CheckpointConfig

from aicc_tools.utils.utils import get_net_outputs


class LossMonitor(Callback):
    """
    Monitor the loss in training.

    If the loss is NAN or INF, it will terminate training.

    Note:
        If per_print_times is 0, do not print loss.

    Args:
        per_print_times (int): How many steps to print once loss. During sink mode, it will print loss in the
                               nearest step. Default: 1.

    Raises:
        ValueError: If per_print_times is not an integer or less than zero.
        ValueError: If data_size is not an integer or less than zero.
    """

    def __init__(self, per_print_times=1, data_size=None, log=logger):
        super(LossMonitor, self).__init__()
        if not isinstance(per_print_times, int) or per_print_times < 0:
            raise ValueError("The argument 'per_print_times' must be int and >= 0, "
                             "but got {}".format(per_print_times))
        self._per_print_times = per_print_times
        self._last_print_time = 0
        self.data_size = data_size
        self.step_time = time.time()
        self.log = log

    def step_begin(self, run_context):
        """
        Record time at the begin of step.

        Args:
            run_context (RunContext): Context of the train running.
        """
        self.step_time = time.time()

    def step_end(self, run_context):
        """
        Print training loss at the end of step.

        Args:
            run_context (RunContext): Context of the train running.
        """
        cb_params = run_context.original_args()

        step_seconds = (time.time() - self.step_time) * 1000

        loss = get_net_outputs(cb_params.net_outputs)

        cur_step_in_epoch = (cb_params.cur_step_num - 1) % cb_params.batch_num + 1

        if isinstance(loss, float) and (np.isnan(loss) or np.isinf(loss)):
            raise ValueError('epoch: {} step: {}. Invalid loss, terminating training.'.format(
                cb_params.cur_epoch_num, cur_step_in_epoch))
        if self._per_print_times != 0 and (cb_params.cur_step_num - self._last_print_time) >= self._per_print_times:
            self._last_print_time = cb_params.cur_step_num
            self.log.info('epoch: {} step: {}, loss is {}; per step time: {:5.3f} ms'.format(
                cb_params.cur_epoch_num, cur_step_in_epoch, loss, step_seconds))


class CheckpointMointor:
    """
    Args:
        prefix (str): The prefix name of checkpoint files. Default: "CKP".
        directory (str): The path of the folder which will be saved in the checkpoint file.
            By default, the file is saved in the current directory. Default: None.
        config (CheckpointConfig): Checkpoint strategy configuration. Default: None.
        save_checkpoint_steps (int): Steps to save checkpoint. Default: 1.
        save_checkpoint_seconds (int): Seconds to save checkpoint.
            Can't be used with save_checkpoint_steps at the same time. Default: 0.
        keep_checkpoint_max (int): Maximum number of checkpoint files can be saved. Default: 5.
        keep_checkpoint_per_n_minutes (int): Save the checkpoint file every `keep_checkpoint_per_n_minutes` minutes.
            Can't be used with keep_checkpoint_max at the same time. Default: 0.
        integrated_save (bool): Whether to merge and save the split Tensor in the automatic parallel scenario.
            Integrated save function is only supported in automatic parallel scene, not supported
            in manual parallel. Default: True.
        async_save (bool): Whether asynchronous execution saves the checkpoint to a file. Default: False.
        saved_network (Cell): Network to be saved in checkpoint file. If the saved_network has no relation
            with the network in training, the initial value of saved_network will be saved. Default: None.
        append_info (list): The information save to checkpoint file. Support "epoch_num", "step_num" and dict.
            The key of dict must be str, the value of dict must be one of int float and bool. Default: None.
        enc_key (Union[None, bytes]): Byte type key used for encryption. If the value is None, the encryption
                                      is not required. Default: None.
        enc_mode (str): This parameter is valid only when enc_key is not set to None. Specifies the encryption
                        mode, currently supports 'AES-GCM' and 'AES-CBC'. Default: 'AES-GCM'.
        exception_save (bool): Whether to save the current checkpoint when an exception occurs. Default: False.

    Raises:
        ValueError: If input parameter is not the correct type.
        ValueError: If the prefix is invalid.
        TypeError: If the config is not CheckpointConfig type.
    """
    def __init__(self,
                 prefix='CKP',
                 directory=None,
                 config=None,
                 save_checkpoint_steps=1,
                 save_checkpoint_seconds=0,
                 keep_checkpoint_max=5,
                 keep_checkpoint_per_n_minutes=0,
                 integrated_save=True,
                 async_save=False,
                 saved_network=None,
                 append_info=None,
                 enc_key=None,
                 enc_mode='AES-GCM',
                 exception_save=False
                 ):
        self.prefix = prefix
        self.directory = directory
        self.config = config
        self.save_checkpoint_steps = save_checkpoint_steps
        self.save_checkpoint_seconds = save_checkpoint_seconds
        self.keep_checkpoint_max = keep_checkpoint_max
        self.keep_checkpoint_per_n_minutes = keep_checkpoint_per_n_minutes
        self.integrated_save = integrated_save
        self.async_save = async_save
        self.saved_network = saved_network
        self.append_info = append_info
        self.enc_key = enc_key
        self.enc_mode = enc_mode
        self.exception_save = exception_save

    def save_checkpoint(self):
        config_ck = CheckpointConfig(save_checkpoint_steps=self.save_checkpoint_steps,
                                     save_checkpoint_seconds=self.save_checkpoint_seconds,
                                     keep_checkpoint_max=self.keep_checkpoint_max,
                                     keep_checkpoint_per_n_minutes=self.keep_checkpoint_per_n_minutes,
                                     integrated_save=self.integrated_save,
                                     async_save=self.async_save,
                                     saved_network=self.saved_network,
                                     append_info=self.append_info,
                                     enc_key=self.enc_key,
                                     enc_mode=self.enc_mode,
                                     exception_save=self.exception_save)
        ckpoint_cb = ModelCheckpoint(prefix=self.prefix,
                                     directory=self.directory,
                                     config=config_ck)
        return ckpoint_cb


class ProfileMonitor(Callback):
    """
    Profile analysis in training.
    """
    def __init__(self, start_step=0, stop_step=10, output_path=None, profile_communication=False):
        super(ProfileMonitor, self).__init__()
        self.start_step = start_step
        self.stop_step = stop_step
        if output_path is not None:
            self.profiler = Profiler(
                start_profile=False, output_path=output_path, profile_communication=profile_communication)
        else:
            self.profiler = Profiler(start_profile=False)

    def step_begin(self, run_context):
        """
        Start profile at the begin of step.

        Args:
            run_context (RunContext): Context of the train running.
        """
        cb_params = run_context.original_args()
        step_num = cb_params.cur_step_num
        if step_num == self.start_step:
            self.profiler.start()

    def step_end(self, run_context):
        """
        Stop profile at the end of step.

        Args:
            run_context (RunContext): Context of the train running.
        """
        cb_params = run_context.original_args()
        step_num = cb_params.cur_step_num
        if step_num == self.stop_step:
            self.profiler.stop()

    def end(self, run_context):
        """
        Collect profile info at the end of training.

        Args:
            run_context (RunContext): Context of the train running.
        """
        self.profiler.analyse()
