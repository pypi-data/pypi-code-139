import os as _os
from . import base as __base


def file(__name: str, is_abspath: bool = False):
    path = __base.abspath(__name, is_abspath)
    return _os.path.isfile(path)


def dir(__name: str, is_abspath: bool = False):
    path = __base.abspath(__name, is_abspath)
    return _os.path.isdir(path)
