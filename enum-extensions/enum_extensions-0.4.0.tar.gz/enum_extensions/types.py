from threading import Lock
from typing import Any, Type, TypeVar, Union

from solus import Singleton
from typing_extensions import TypeGuard

__all__ = (
    "Null",
    "Nullable",
    "null",
    "is_null",
    "is_not_null",
)

T = TypeVar("T")


class Null(Singleton):
    pass


null = Null()

Nullable = Union[T, Null]


def is_null(item: Nullable[T]) -> TypeGuard[Null]:
    return item is null


def is_not_null(item: Nullable[T]) -> TypeGuard[T]:
    return item is not null
