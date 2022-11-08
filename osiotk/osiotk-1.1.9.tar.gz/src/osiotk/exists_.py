import os as _os
from . import base as __base
from . import is_ as __is


def node(__name: str, is_abspath: bool = False):
    path = __base.abspath(__name, is_abspath)
    return _os.path.exists(path)


def file(__name: str, is_abspath: bool = False):
    path = __base.abspath(__name, is_abspath)
    return node(path, is_abspath=True) and __is.file(path, is_abspath=True)


def dir(__name: str, is_abspath: bool = False):
    path = __base.abspath(__name, is_abspath)
    return node(path, is_abspath=True) and __is.dir(path, is_abspath=True)
