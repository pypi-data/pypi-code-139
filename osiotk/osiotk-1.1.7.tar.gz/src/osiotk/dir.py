import os as __os
from typing import Callable, Optional
from . import path as __ospath

FilePredicate = Callable[[__os.DirEntry], bool]


def __scan(__path: str, __where: Optional[FilePredicate]):
    return (
        (file for file in __os.scandir(__path))
        if __where is None
        else (file for file in __os.scandir(__path) if __where(file))
    )


def __count(__path, __where: Optional[FilePredicate] = None):
    result = 0
    for _ in __scan(__path, __where):
        result += 1
    return result


def __remove_path(__path: str | __os.DirEntry):
    path = __path.path if isinstance(__path, __os.DirEntry) else __path
    if __os.path.exists(path):
        __os.remove(path)


def __dirfiles(__path: str, abs_paths: bool = True):
    result = [
        file
        for file in __os.listdir(__path)
        if __ospath.isfile(__ospath.join(__path, file))
    ]
    if abs_paths:
        result = [__ospath.join(__path, file) for file in result]
    return result


def __mostrecentpath(__path: str):
    return max(__dirfiles(__path), key=__ospath.created_at)


def __oldestpath(__path: str):
    return min(__dirfiles(__path), key=__ospath.created_at)


def count(__path, __where: Optional[FilePredicate] = None):
    return __count(__path, __where)


def remove_path(__path: str | __os.DirEntry):
    return __remove_path(__path)


def scan(__path: str, __where: Optional[FilePredicate] = None):
    return __scan(__path, __where)


def mostrecentpath(__path: str):
    return __mostrecentpath(__path)


def oldestpath(__path: str):
    return __oldestpath(__path)
