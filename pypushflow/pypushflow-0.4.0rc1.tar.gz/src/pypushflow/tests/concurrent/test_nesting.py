import pytest
from . import utils
from . import filter_combinations


@pytest.mark.parametrize("scaling", [True, False])
@pytest.mark.parametrize("pool_type", utils.POOLS)
@pytest.mark.parametrize("task_name", list(utils.SUCCESS))
@pytest.mark.parametrize("context", utils.CONTEXTS)
def test_callback(scaling, pool_type, task_name, context):
    with utils.pool_context(scaling, pool_type, context=context) as pool:
        with filter_combinations.filter_callback(pool_type, task_name, context):
            utils.assert_callback(pool, task_name)


@pytest.mark.parametrize("scaling", [True, False])
@pytest.mark.parametrize("pool_type", utils.POOLS)
@pytest.mark.parametrize("task_name", list(utils.FAILURE))
@pytest.mark.parametrize("context", utils.CONTEXTS)
def test_error_callback(scaling, pool_type, task_name, context):
    with utils.pool_context(scaling, pool_type, context=context) as pool:
        with filter_combinations.filter_error_callback(pool_type, task_name, context):
            utils.assert_error_callback(pool, task_name)
