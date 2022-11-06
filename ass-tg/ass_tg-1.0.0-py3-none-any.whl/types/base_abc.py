from abc import ABC
from typing import Any, Generic, Iterable, Optional, Tuple, TypeVar

from aiogram.types import MessageEntity
from babel.support import LazyProxy

from ass.exceptions import ArgIsRequiredError, ArgTypeError

ArgValueType = TypeVar('ArgValueType')


class ArgFabric(Generic[ArgValueType]):
    """Provides a way to create an argument fabric."""
    description: Optional[LazyProxy]

    # Some parameters used by the other arguments
    know_the_end: bool = False
    default_no_value_value: Optional[Any] = None

    def __init__(self, description: Optional[LazyProxy] = None):
        self.description = description

    @property
    def needed_type(self) -> Tuple[LazyProxy, LazyProxy]:
        raise NotImplementedError

    @staticmethod
    def check(raw_text: str) -> bool:
        """
        Checks if the given text is valid for this type.
        It should check by the start of the text, as it could contain other arguments separated.
        """
        raise NotImplementedError

    def parse(self, text: str, entities: Optional[Iterable[MessageEntity]] = None) -> Tuple[int, ArgValueType]:
        """Parses the arguments texts and returns the length of argument and value.
        Returns None if there's no more arguments."""

        raise NotImplementedError

    def pre_parse(self, *args, **_kwargs):
        return self.parse(*args)

    def __call__(self, text: str, offset: int, **kwargs) -> "ParsedArg":
        if not self.check(text):
            raise ArgIsRequiredError(description=self.description)

        length, value = self.pre_parse(text, **kwargs)
        return ParsedArg(self, value, offset, length)

    def __repr__(self):
        return f"<{self.__class__.__name__}>"


ParsedArgType = TypeVar('ParsedArgType')


class ParsedArg(ABC, Generic[ParsedArgType]):
    """Argument object."""

    fabric: ArgFabric
    value: ParsedArgType

    offset: int
    length: int

    def __init__(self, fabric: ArgFabric, value: ParsedArgType, offset: int, length: int):
        self.fabric = fabric
        self.value = value
        self.offset = offset
        self.length = length

    @property
    def values(self) -> Tuple[ParsedArgType]:
        if not isinstance(self.value, list):
            raise TypeError("Value must be a ArgFabric")

        return tuple(x.value for x in self.value)

    def __repr__(self):
        return f"<{self.fabric}: {self.value=} {self.length=}>"


class OneWordArgFabricABC(ArgFabric, ABC):
    needed_type: Tuple[LazyProxy, LazyProxy]
    args_separator: str = ' '

    def check_type(self, text: str) -> bool:
        raise NotImplementedError

    def check(self, text: str) -> bool:
        return text.lstrip() != ""

    def value(self, text: str) -> Any:
        raise NotImplementedError

    def parse(self, raw_text: str, entities: Optional[Iterable[MessageEntity]] = None) -> Tuple[int, Any]:
        first_word, *_rest = raw_text.split(self.args_separator, 1)

        if not self.check_type(first_word):
            raise ArgTypeError(text=first_word, needed_type=self.needed_type, description=self.description)

        return len(first_word), self.value(first_word)
