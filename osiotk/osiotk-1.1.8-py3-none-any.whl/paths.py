from collections import defaultdict as _defaultdict
import os as _os
from . import base as __base
from . import exists_ as __exists


def safepath(__name: str, is_abspath: bool = False, exist_ok: bool = True):
    path = __base.abspath(__name, is_abspath)
    dirname = __base.parentdir(path, True)
    if not __exists.dir(dirname, is_abspath=True):
        _os.makedirs(dirname, exist_ok=exist_ok)
    return path


def filetree(__ft: str, parentdir: str = None, indent: int = 4) -> list[str]:
    paths: list[str] = []
    dirlog = _defaultdict(list[str])
    for line in (line for line in __ft.splitlines(keepends=False) if line):
        offset, path = len(line) - len(line.lstrip()), line.strip()
        dirlog[offset].append(path)
        while offset > 0:
            if dirlog[offset - indent]:
                path = f"{dirlog[offset-indent][-1]}/{path}"
            offset -= indent
        if path:
            paths.append(path)
    if parentdir is not None and parentdir:
        for (i, path) in enumerate(paths):
            if len(path) - len(path.lstrip()) == 0:
                paths[i] = __base.join_paths(parentdir, path)
    return paths
