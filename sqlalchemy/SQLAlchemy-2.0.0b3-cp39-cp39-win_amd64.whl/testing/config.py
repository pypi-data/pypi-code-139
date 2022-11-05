# testing/config.py
# Copyright (C) 2005-2022 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php
# mypy: ignore-errors


from __future__ import annotations

import collections
import typing
from typing import Any
from typing import Callable
from typing import Iterable
from typing import Optional
from typing import Tuple
from typing import TypeVar
from typing import Union

from .. import util

requirements = None
db = None
db_url = None
db_opts = None
file_config = None
test_schema = None
test_schema_2 = None
any_async = False
_current = None
ident = "main"

if typing.TYPE_CHECKING:
    from .plugin.plugin_base import FixtureFunctions

    _fixture_functions: FixtureFunctions
else:
    _fixture_functions = None  # installed by plugin_base


_FN = TypeVar("_FN", bound=Callable[..., Any])


def combinations(
    *comb: Union[Any, Tuple[Any, ...]],
    argnames: Optional[str] = None,
    id_: Optional[str] = None,
    **kw: str,
) -> Callable[[_FN], _FN]:
    r"""Deliver multiple versions of a test based on positional combinations.

    This is a facade over pytest.mark.parametrize.


    :param \*comb: argument combinations.  These are tuples that will be passed
     positionally to the decorated function.

    :param argnames: optional list of argument names.   These are the names
     of the arguments in the test function that correspond to the entries
     in each argument tuple.   pytest.mark.parametrize requires this, however
     the combinations function will derive it automatically if not present
     by using ``inspect.getfullargspec(fn).args[1:]``.  Note this assumes the
     first argument is "self" which is discarded.

    :param id\_: optional id template.  This is a string template that
     describes how the "id" for each parameter set should be defined, if any.
     The number of characters in the template should match the number of
     entries in each argument tuple.   Each character describes how the
     corresponding entry in the argument tuple should be handled, as far as
     whether or not it is included in the arguments passed to the function, as
     well as if it is included in the tokens used to create the id of the
     parameter set.

     If omitted, the argument combinations are passed to parametrize as is.  If
     passed, each argument combination is turned into a pytest.param() object,
     mapping the elements of the argument tuple to produce an id based on a
     character value in the same position within the string template using the
     following scheme::

        i - the given argument is a string that is part of the id only, don't
            pass it as an argument

        n - the given argument should be passed and it should be added to the
            id by calling the .__name__ attribute

        r - the given argument should be passed and it should be added to the
            id by calling repr()

        s - the given argument should be passed and it should be added to the
            id by calling str()

        a - (argument) the given argument should be passed and it should not
            be used to generated the id

     e.g.::

        @testing.combinations(
            (operator.eq, "eq"),
            (operator.ne, "ne"),
            (operator.gt, "gt"),
            (operator.lt, "lt"),
            id_="na"
        )
        def test_operator(self, opfunc, name):
            pass

    The above combination will call ``.__name__`` on the first member of
    each tuple and use that as the "id" to pytest.param().


    """
    return _fixture_functions.combinations(
        *comb, id_=id_, argnames=argnames, **kw
    )


def combinations_list(
    arg_iterable: Iterable[
        Tuple[
            Any,
        ]
    ],
    **kw,
):
    "As combination, but takes a single iterable"
    return combinations(*arg_iterable, **kw)


def fixture(*arg: Any, **kw: Any) -> Any:
    return _fixture_functions.fixture(*arg, **kw)


def get_current_test_name() -> str:
    return _fixture_functions.get_current_test_name()


def mark_base_test_class() -> Any:
    return _fixture_functions.mark_base_test_class()


class _AddToMarker:
    def __getattr__(self, attr: str) -> Any:
        return getattr(_fixture_functions.add_to_marker, attr)


add_to_marker = _AddToMarker()


class Config:
    def __init__(self, db, db_opts, options, file_config):
        self._set_name(db)
        self.db = db
        self.db_opts = db_opts
        self.options = options
        self.file_config = file_config
        self.test_schema = "test_schema"
        self.test_schema_2 = "test_schema_2"

        self.is_async = db.dialect.is_async and not util.asbool(
            db.url.query.get("async_fallback", False)
        )

    _stack = collections.deque()
    _configs = set()

    def _set_name(self, db):
        suffix = "_async" if db.dialect.is_async else ""
        if db.dialect.server_version_info:
            svi = ".".join(str(tok) for tok in db.dialect.server_version_info)
            self.name = "%s+%s%s_[%s]" % (db.name, db.driver, suffix, svi)
        else:
            self.name = "%s+%s%s" % (db.name, db.driver, suffix)

    @classmethod
    def register(cls, db, db_opts, options, file_config):
        """add a config as one of the global configs.

        If there are no configs set up yet, this config also
        gets set as the "_current".
        """
        global any_async

        cfg = Config(db, db_opts, options, file_config)

        # if any backends include an async driver, then ensure
        # all setup/teardown and tests are wrapped in the maybe_async()
        # decorator that will set up a greenlet context for async drivers.
        any_async = any_async or cfg.is_async

        cls._configs.add(cfg)
        return cfg

    @classmethod
    def set_as_current(cls, config, namespace):
        global db, _current, db_url, test_schema, test_schema_2, db_opts
        _current = config
        db_url = config.db.url
        db_opts = config.db_opts
        test_schema = config.test_schema
        test_schema_2 = config.test_schema_2
        namespace.db = db = config.db

    @classmethod
    def push_engine(cls, db, namespace):
        assert _current, "Can't push without a default Config set up"
        cls.push(
            Config(
                db, _current.db_opts, _current.options, _current.file_config
            ),
            namespace,
        )

    @classmethod
    def push(cls, config, namespace):
        cls._stack.append(_current)
        cls.set_as_current(config, namespace)

    @classmethod
    def pop(cls, namespace):
        if cls._stack:
            # a failed test w/ -x option can call reset() ahead of time
            _current = cls._stack[-1]
            del cls._stack[-1]
            cls.set_as_current(_current, namespace)

    @classmethod
    def reset(cls, namespace):
        if cls._stack:
            cls.set_as_current(cls._stack[0], namespace)
            cls._stack.clear()

    @classmethod
    def all_configs(cls):
        return cls._configs

    @classmethod
    def all_dbs(cls):
        for cfg in cls.all_configs():
            yield cfg.db

    def skip_test(self, msg):
        skip_test(msg)


def skip_test(msg):
    raise _fixture_functions.skip_test_exception(msg)


def async_test(fn):
    return _fixture_functions.async_test(fn)
