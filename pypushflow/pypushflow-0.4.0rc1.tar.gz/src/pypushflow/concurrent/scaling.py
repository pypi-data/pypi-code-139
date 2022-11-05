from numbers import Number
from typing import Callable, Optional
from .base import BasePool


class ScalingPool(BasePool):
    def __init__(
        self,
        wait_on_exit: bool = True,
        wait_on_exit_timeout: Optional[Number] = None,
        pool_type: Optional[str] = None,
        **pool_options,
    ):
        if pool_type == "scaling":
            raise ValueError("cannot nest scaling pools")
        self._running_pools = list()
        self._finished_pools = list()
        self._pool_type = pool_type
        pool_options["max_workers"] = 1
        self._pool_options = pool_options
        super().__init__(
            wait_on_exit=wait_on_exit, wait_on_exit_timeout=wait_on_exit_timeout
        )

    def close(self):
        self._close_running_pools()
        self._close_finished_pools()

    def join(self, timeout: Optional[Number] = None):
        return self._join_running_pools(timeout=timeout) and self._join_finished_pools(
            timeout=timeout
        )

    def terminate(self, block: bool = False, timeout: Optional[Number] = None):
        self._terminate_running_pools(block=block, timeout=timeout)
        self._terminate_finished_pools(block=block, timeout=timeout)

    def _new_pool(self):
        from .factory import get_pool

        pool = get_pool(self._pool_type)(**self._pool_options)
        self._running_pools.append(pool)
        return pool

    def _release_pool(self, pool):
        try:
            idx = self._running_pools.index(pool)
        except ValueError:
            return
        pool = self._running_pools.pop(idx)
        self._finished_pools.append(pool)

    def _close_finished_pools(self):
        for pool in self._finished_pools:
            pool.close()

    def _close_running_pools(self):
        for pool in self._running_pools:
            pool.close()

    def _join_finished_pools(self, timeout: Optional[Number] = None):
        return all(pool.join(timeout=timeout) for pool in self._finished_pools)

    def _join_running_pools(self, timeout: Optional[Number] = None):
        return all(pool.join(timeout=timeout) for pool in self._running_pools)

    def _terminate_finished_pools(
        self, block: bool = True, timeout: Optional[Number] = None
    ):
        if block:
            while self._finished_pools:
                pool = self._finished_pools.pop(0)
                try:
                    pool.terminate(block=block, timeout=timeout)
                except BaseException:
                    self._finished_pools.append(pool)
                    raise
        else:
            for pool in self._finished_pools:
                pool.terminate(block=block, timeout=timeout)

    def _terminate_running_pools(
        self, block: bool = True, timeout: Optional[Number] = None
    ):
        if block:
            while self._running_pools:
                pool = self._running_pools.pop(0)
                try:
                    pool.terminate(block=block, timeout=timeout)
                except BaseException:
                    self._running_pools.append(pool)
                    raise
        else:
            for pool in self._running_pools:
                pool.terminate(block=block, timeout=timeout)

    def apply_async(
        self,
        fn: Callable,
        callback: Optional[Callable] = None,
        error_callback: Optional[Callable] = None,
        args=tuple(),
        kwargs=None,
    ):
        pool = self._new_pool()

        if callback is None:

            def _callback(return_value):
                self._release_pool(pool)

        else:

            def _callback(return_value):
                try:
                    return callback(return_value)
                finally:
                    self._release_pool(pool)

        if callback is None:

            def _error_callback(exception):
                self._release_pool(pool)

        else:

            def _error_callback(exception):
                try:
                    return error_callback(exception)
                finally:
                    self._release_pool(pool)

        future = pool.apply_async(
            fn,
            args=args,
            kwargs=kwargs,
            callback=_callback,
            error_callback=_error_callback,
        )
        pool.close()
        return future
