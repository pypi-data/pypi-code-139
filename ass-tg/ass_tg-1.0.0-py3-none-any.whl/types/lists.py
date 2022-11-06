from typing import Any, Generic, Iterable, List, Optional, Tuple, TypeVar

from aiogram.types import MessageEntity
from babel.support import LazyProxy
from stfu_tg import Code

from ass.exceptions import (ArgCustomError, ArgInListItemError, ArgListEmpty, ArgTypeError)
from ass.types.wrapped import WrappedArgFabricABC
from ass.i18n import gettext as _

ListArgItemType = TypeVar('ListArgItemType')


class ListArg(WrappedArgFabricABC[List[Any]], Generic[ListArgItemType]):
    # TODO: Make folded lists working
    list_separator: str
    list_start: str
    list_end: str

    def __init__(self, *args, separator=',', list_start='(', list_end=')'):
        super().__init__(*args)

        self.list_separator = separator
        self.list_start = list_start
        self.list_end = list_end

    @property
    def needed_type(self) -> Tuple[LazyProxy, LazyProxy]:
        # TODO: Show settings??
        return (
            # Here we use plural, because lists contains many items
            LazyProxy(lambda: _("List of {}").format(self.child_fabric.needed_type[1])),
            LazyProxy(lambda: _("Lists of {}").format(self.child_fabric.needed_type[1]))
        )

    def check(self, text: str) -> bool:
        if not (text.startswith(self.list_start) and self.list_end in text):
            raise ArgTypeError(text=text, needed_type=self.needed_type, description=self.description)

        if text.find(self.list_start) + 1 == text.find(self.list_end):
            raise ArgListEmpty(needed_type=self.needed_type, description=self.description)
        return True

    def parse(self, text: str, entities: Optional[Iterable[MessageEntity]] = None) -> Tuple[int, List[ListArgItemType]]:
        text = text.removeprefix(self.list_start).replace(self.list_end, '')

        items = []

        # Add syntax symbols to length initially
        length = len(self.list_start) + len(self.list_end)

        while text:
            separator_index = text.find(self.list_separator)
            has_separator = separator_index != -1

            arg_text = text if self.child_fabric.know_the_end or not has_separator else text[:separator_index]

            try:
                arg = self.child_fabric(
                    arg_text,
                    length,
                    known_end_arg_text=text,
                    not_known_end_arg_text=text[:separator_index] if has_separator else text)

            except ArgTypeError as e:
                raise ArgInListItemError(e) from e

            items.append(arg)
            length += arg.length

            if not self.child_fabric.know_the_end:
                text = text[separator_index + 1:] if has_separator else ''
                length += (len(text) - len(text := text.lstrip()))

                # Calculate the number of extra symbols that wasn't occupied by the argument
                if has_separator:
                    length += len(arg_text[arg.length:])
                    length += len(self.list_separator)
            else:
                text = text[arg.length:]

                length += (len(text) - len(text := text.lstrip()))

                if text.find(self.list_separator) != -1 and not text.startswith(self.list_separator):
                    raise ArgCustomError(LazyProxy(lambda: _(
                        "Argument in list ({arg_text}) was parsed, but it has unknown text after it ({rest_rext}). "
                        "Please ensure you correctly divided all of arguments."
                    ).format(
                        arg_text=Code(arg_text[:arg.length]),
                        rest_rext=Code(arg_text[arg.length:])
                    )))

                length += (len(text) - len(text := text.removeprefix(self.list_separator).lstrip()))

            if not has_separator:
                # No more separators - returning
                break

            if not arg.length and not text:
                # Argument has no length, and no text left - Means this argument consumes all text
                break

        return length, items


class DividedArg(ListArg):

    def __init__(self, *args, separator='|'):
        super().__init__(*args, separator=separator, list_start='', list_end='')
