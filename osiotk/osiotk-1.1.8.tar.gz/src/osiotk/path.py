from os import path as __ospath


def __join(__a: str, *paths):
    return __ospath.join(__a, *paths)


def __isfile(__path: str):
    return __ospath.isfile(__path)


def __created_at(__path: str):
    return __ospath.getctime(__path)


def join(__a: str, *paths):
    return __join(__a, *paths)


def isfile(__path: str):
    return __isfile(__path)


def created_at(__path: str):
    return __created_at(__path)
