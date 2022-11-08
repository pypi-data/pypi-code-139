from typing import Callable
from . import base as __base
from . import is_ as __is
from . import make as __mk
from . import read as __read
from . import exists_ as __exists
from . import write_ as __write
from . import path
from . import dir


def system(__command: str):
    return __base.system(__command)


def join_paths(__base, branch):
    return __base.join_paths(__base, branch)


def abspath(__name: str, is_abspath: bool = False):
    return __base.abspath(__name, is_abspath=is_abspath)


def basename(__name: str):
    return __base.basename(__name)


def parentdir(__name: str, is_abspath: bool = False):
    return __base.parentdir(__name, is_abspath)


def scandir(__name: str, is_abspath: bool, where: Callable[[object], bool] = None):
    return __base.scandir(__name, is_abspath=is_abspath, where=where)


def isfile(__name: str, is_abspath: bool = False):
    return __is.file(__name, is_abspath=is_abspath)


def isdir(__name: str, is_abspath: bool = False):
    return __is.dir(__name, is_abspath)


def exists(__name: str, is_abspath: bool = False):
    return __exists.node(__name, is_abspath)


def file_exists(__name: str, is_abspath: bool = False):
    return __exists.file(__name, is_abspath)


def dir_exists(__name: str, is_abspath: bool = False):
    return __exists.dir(__name, is_abspath)


def mkdir(__name: str, is_abspath: bool = False, exist_ok: bool = True):
    return __mk.dir(__name, is_abspath=is_abspath, exist_ok=exist_ok)


def mkfile(__name: str, is_abspath: bool = False):
    return __mk.file(__name, is_abspath)


def reads(__name: str, is_abspath: bool = False):
    return __read.string(__name, is_abspath)


def readb(__name: str, is_abspath: bool = False):
    return __read.bytes(__name, is_abspath)


def readjson(__name: str, is_abspath: bool = False):
    return __read.json(__name, is_abspath)


def readlines(
    __name: str,
    is_abspath: bool = False,
    keepends: bool = False,
    where: Callable[[str], bool] = None,
):
    return __read.lines(__name, is_abspath=is_abspath, keepends=keepends, where=where)


def writes(
    __name: str,
    content: str,
    is_abspath: bool = False,
    errors: str = "ignore",
    encoding: str = "utf-8",
    exist_ok: bool = True,
):
    return __write.string(
        __name,
        content=content,
        is_abspath=is_abspath,
        errors=errors,
        encoding=encoding,
        exist_ok=exist_ok,
    )


def writeb(
    __name: str,
    content: bytes,
    is_abspath: bool = False,
    errors: str = "ignore",
    encoding: str = "utf-8",
    exist_ok: bool = True,
):
    return __write.bytes(
        __name,
        content=content,
        is_abspath=is_abspath,
        errors=errors,
        encoding=encoding,
        exist_ok=exist_ok,
    )


def writejson(
    __name: str,
    content,
    indent: int = 4,
    is_abspath: bool = False,
    exist_ok: bool = True,
):
    return __write.json(
        __name, content=content, indent=indent, is_abspath=is_abspath, exist_ok=exist_ok
    )


def writedata(
    __name: str,
    content,
    indent: int = 4,
    is_abspath: bool = False,
    errors: str = "ignore",
    encoding: str = "utf-8",
    exist_ok: bool = True,
):
    return __write.data(
        __name,
        content=content,
        indent=indent,
        is_abspath=is_abspath,
        errors=errors,
        encoding=encoding,
        exist_ok=exist_ok,
    )


def mk_filetree(
    __ft: str, overwrite_if_exists: bool = False, parentdir: str = None, indent: int = 4
):
    return __mk.filetree(
        __ft,
        overwrite_if_exists=overwrite_if_exists,
        parentdir=parentdir,
        indent=indent,
    )


if __name__ == "__main__":
    for imported_module in (path, dir):
        if imported_module is None:
            raise ImportError(
                f"osiotk.error: failed to import submodule {imported_module.__name__}"
            )
