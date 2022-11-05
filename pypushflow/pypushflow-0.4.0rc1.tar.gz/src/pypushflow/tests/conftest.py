import pytest
import psutil
import logging


logger = logging.getLogger(__name__)


@pytest.fixture()
def workflow_cleanup():
    current_process = psutil.Process()
    subprocesses = {child.pid for child in current_process.children(recursive=True)}
    fail_on_subprocesses = True
    yield
    has_new_subprocesses = False
    for child in current_process.children(recursive=True):
        if child.pid not in subprocesses:
            has_new_subprocesses = True
            logger.error("dangling child %s", child)
            try:
                child.terminate()
            except psutil.NoSuchProcess:
                pass
    if has_new_subprocesses and fail_on_subprocesses:
        raise RuntimeError("not all subprocesses have finished")
