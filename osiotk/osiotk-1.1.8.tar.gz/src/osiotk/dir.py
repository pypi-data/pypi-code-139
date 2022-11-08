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


def __dirfiles(
    __path: str, __where: Optional[FilePredicate] = None, abs_paths: bool = True
):
    predicate = lambda __file: __ospath.isfile(__ospath.join(__path, __file))
    if __where is not None:
        base = predicate
        predicate = lambda __file: __where(__file) and base(__file)

    result = [file for file in __os.listdir(__path) if predicate(file)]

    if abs_paths:
        result = [__ospath.join(__path, file) for file in result]
    return result


def __mostrecentpath(__path: str, __where: Optional[FilePredicate] = None):
    return max(__dirfiles(__path, __where), key=__ospath.created_at)


def __oldestpath(__path: str, __where: Optional[FilePredicate] = None):
    return min(__dirfiles(__path, __where), key=__ospath.created_at)


def __scan_sorted_by_created_at(
    __path: str, __where: Optional[FilePredicate], abs_paths: bool, reverse: bool
):
    filesin = __dirfiles(__path, __where, abs_paths=abs_paths)
    filesin.sort(key=__ospath.created_at, reverse=reverse)
    return iter(filesin)


def __scan_oldest_to_mostrecent(
    __path: str, __where: Optional[FilePredicate], abs_paths: bool
):
    return __scan_sorted_by_created_at(
        __path, __where, abs_paths=abs_paths, reverse=False
    )


def __scan_mostrecent_to_oldest(
    __path: str, __where: Optional[FilePredicate], abs_paths: bool
):
    return __scan_sorted_by_created_at(
        __path, __where, abs_paths=abs_paths, reverse=True
    )


def count(__path, __where: Optional[FilePredicate] = None):
    return __count(__path, __where)


def remove_path(__path: str | __os.DirEntry):
    return __remove_path(__path)


def scan(__path: str, __where: Optional[FilePredicate] = None):
    return __scan(__path, __where)


def scan_oldest_to_mostrecent(
    __path: str, __where: Optional[FilePredicate] = None, abs_paths: bool = True
):
    return __scan_oldest_to_mostrecent(__path, __where, abs_paths=abs_paths)


def scan_mostrecent_to_oldest(
    __path: str, __where: Optional[FilePredicate] = None, abs_paths: bool = True
):
    return __scan_mostrecent_to_oldest(__path, __where, abs_paths=abs_paths)


def mostrecentpath(__path: str):
    return __mostrecentpath(__path)


def oldestpath(__path: str):
    return __oldestpath(__path)
