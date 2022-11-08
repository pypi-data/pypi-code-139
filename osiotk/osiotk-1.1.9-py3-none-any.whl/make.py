import os as _os
from . import base as __base
from . import write_ as __write
from . import exists_ as __exists
from . import paths as _paths


def dir(__name: str, is_abspath: bool = False, exist_ok: bool = True):
    path = __base.abspath(__name, is_abspath)
    if not __exists.dir(path, is_abspath=True):
        _os.makedirs(path, exist_ok=exist_ok)


def file(__name: str, is_abspath: bool = False):
    path = __base.abspath(__name, is_abspath)
    if not __exists.file(path, True):
        __write.string(path, content="", is_abspath=True)


def filetree(
    __ft: str, overwrite_if_exists: bool = False, parentdir: str = None, indent: int = 4
):
    ft_paths = _paths.filetree(__ft, parentdir=parentdir, indent=indent)
    dirpaths = set(
        path
        for path in ft_paths
        if (
            next(
                (
                    ft_path
                    for ft_path in ft_paths
                    if (ft_path.startswith(f"{path}/") and ft_path != path)
                ),
                None,
            )
            is not None
        )
        and not "." in __base.basename(path)
    )
    for dirpath in dirpaths:
        dir(dirpath)

    for path in ft_paths:
        if not path in dirpaths:
            if __exists.file(path):
                if overwrite_if_exists:
                    __write.string(path, content="")
            else:
                file(path)

    for path in ft_paths:
        if not __exists.node(path):
            print(f"error: path does not exist:{path}")
