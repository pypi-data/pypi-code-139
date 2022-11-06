from typing import Tuple

from babel.support import LazyProxy

from ass.exceptions import ArgTypeError
from ass.types.base_abc import ArgFabric
from ass.i18n import lazy_gettext as l_


class QuotedTextArg(ArgFabric):
    know_the_end = True

    @property
    def needed_type(self) -> Tuple[LazyProxy, LazyProxy]:
        return l_("Text (in double quotes)"), l_("Texts (in double quotes)")

    def check(self, text: str) -> bool:
        if text.startswith('"') and text.find('"', 1) != -1:
            return True

        raise ArgTypeError(text=text, needed_type=self.needed_type, description=self.description)

    def parse(self, text: str) -> Tuple[int, str]:
        argument, _rest = text.removeprefix('"').split('"', 1)

        return len(argument) + 2, argument


class RestTextArg(ArgFabric):

    @property
    def needed_type(self) -> Tuple[LazyProxy, LazyProxy]:
        return l_("Text"), l_("Texts")

    @staticmethod
    def check(text: str) -> bool:
        return text != ""

    def parse(self, text: str) -> Tuple[int, str]:
        return len(text), text
