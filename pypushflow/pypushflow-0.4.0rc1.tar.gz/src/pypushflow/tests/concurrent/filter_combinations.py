from contextlib import contextmanager
import pytest


def gevent_patched() -> bool:
    try:
        from gevent.monkey import is_anything_patched
    except ImportError:
        return False

    return is_anything_patched()


@contextmanager
def filter_callback(pool_type, task_name, context):
    assert pool_type
    assert task_name
    exception = None
    match = None
    if pool_type in ("billiard", "multiprocessing"):
        if gevent_patched():
            pytest.skip("does not work with 'gevent' monkey patching")
        if task_name in ["mppool", "mpprocess", "cfpool"]:
            exception = AssertionError
            match = "daemonic processes are not allowed to have children"
        elif task_name in ["bpool"]:
            pytest.skip("hangs sometimes")
    elif pool_type == "ndmultiprocessing":
        if gevent_patched():
            pytest.skip("does not work with 'gevent' monkey patching")
        if task_name in ["bpool"]:
            pytest.skip("hangs sometimes")
    elif pool_type in ("process", "ndprocess"):
        if gevent_patched():
            if task_name in ["mppool", "bpool"]:
                pytest.skip("pool hangs with gevent")
            if context == "spawn":
                pytest.skip("spawn hangs with gevent")
        else:
            if task_name in ["bpool"]:
                pytest.skip("hangs sometimes")
    elif pool_type == "thread":
        if gevent_patched():
            if task_name in ["mppool", "bpool"]:
                pytest.skip("pool hangs with gevent")
        else:
            if task_name in ["bpool"]:
                pytest.skip("hangs sometimes")
    elif pool_type == "gevent":
        if task_name in ["mppool", "bpool"]:
            pytest.skip("pool hangs with gevent")

    if exception is None:
        yield
    else:
        with pytest.raises(exception, match=match):
            yield


@contextmanager
def filter_error_callback(pool_type, task_name, context):
    assert pool_type
    assert task_name
    if pool_type in ("process", "ndprocess"):
        if gevent_patched():
            if context == "spawn":
                pytest.skip("spawn hangs with gevent")
    yield
