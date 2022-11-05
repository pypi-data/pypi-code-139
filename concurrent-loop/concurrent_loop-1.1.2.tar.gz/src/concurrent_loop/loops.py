#      Concurrent: helper for running functions in a concurrent loop.
#      Copyright (C) 2022  KC Lee  lathe-rebuke.0c@icloud.com
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
Controls concurrent tasks, by threads or multiprocess.
"""
from abc import ABC, abstractmethod
import logging
import multiprocessing
from multiprocessing import Process
import queue
from queue import Empty
from threading import Thread
from time import time

# Set up logging
logging.basicConfig(level=logging.DEBUG)
_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)


class ConcurrentException(Exception):
    """
    General concurrency exception.
    """


class LoopBase(ABC):
    """
    API for running concurrent tasks.
    """
    thread_process = None  # Holds the thread or multiprocess to run.

    _period_ms = None  # Looping periodicity (in concurrent function) in msec.
    _t_next = None  # Target time of next concurrent function loop.

    @property
    @abstractmethod
    def _queue_type(self):
        """
        Queue type to use for communicating into the thread_process. Must be a
        joinable queue type.
        """

    @property
    @abstractmethod
    def _thread_process_type(self):
        """
        Returns:
            cls: Thread or Multiprocess class.
        """

    @property
    def period_ms(self):
        """
        Returns:
            float: Looping periodicity in concurrent function in msec.
        """
        return self._period_ms

    @period_ms.setter
    def period_ms(self, period_ms):
        """
        Sets looping periodicity in concurrent function as float.
        """
        self._period_ms = float(period_ms)

    def __init__(self, period_ms):
        """
        Instantiate and set the looping periodicity.

        Args:
            period_ms (int, float): Looping period in msec.
        """
        self.period_ms = float(period_ms)
        self._t_next = time()
        self._stop_command = self._queue_type()

    def _main_loop_c(self, looped_func, stop_cmd, args):
        """
        The main concurrency loop.

        Args:
            looped_func (func): The function being run as a loop in a
            separate thread of process.
            stop_cmd (Queue): queue.Queue() or multiprocessing.Queue()
            instance through which the stop command is sent through.
            args (tuple): The function arguments.
        """
        self._t_next = time()
        while True:
            try:
                if stop_cmd.get_nowait():
                    _LOGGER.info("Concurrent process terminating.")
                    stop_cmd.task_done()
                    break
            except Empty:
                pass
            t_now = time()
            if t_now >= self._t_next:
                looped_func(*args)
                self._t_next += self.period_ms/1000

    def start(self, looped_func, args=()):
        """
        Starts the concurrent process.

        Args:
            looped_func (func): The function being run as a loop in a
            separate thread of process.
            args (tuple): The function arguments.
        """
        if self.thread_process is None:
            self.thread_process = \
                self._thread_process_type(target=self._main_loop_c,
                                          args=(looped_func,
                                                self._stop_command, args))
            self.thread_process.start()
        else:
            raise ConcurrentException("Concurrent task already running. "
                                      "Stop task before re-initiating.")

    def stop(self):
        """
        Stops the concurrent process
        """
        if self.thread_process is not None:
            _LOGGER.debug("Stopping concurrent task.")
            self._stop_command.put(True)
            self.thread_process.join(0.5)
            while self.thread_process.is_alive():
                _LOGGER.debug("Process ending failed. Re-trying.")
                self._stop_command.put(True)
                try:
                    self.thread_process.kill()  # Works only for Process
                except AttributeError:
                    self.thread_process.join(0.5)  # For Thread.
            self.thread_process = None
            _LOGGER.debug("Concurrent task stopped.")

    def close(self):
        """
        Closing queues.
        """
        if not self._stop_command.empty():
            raise ConcurrentException("Cannot end process - not stopping "
                                      "queue.")
        self._stop_command.join()


class ThreadLoop(LoopBase):
    """
    Creates a thread to run in loops
    """
    _queue_type = queue.Queue
    _thread_process_type = Thread


class ProcessLoop(LoopBase):
    """
    Creates a thread to run in loops
    """
    _queue_type = multiprocessing.JoinableQueue
    _thread_process_type = Process
