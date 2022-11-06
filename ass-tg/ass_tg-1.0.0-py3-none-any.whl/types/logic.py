import contextlib
from typing import Any, Optional, Tuple

from babel.support import LazyProxy

from ass.exceptions import ArgTypeError
from ass.types.base_abc import ArgFabric
from ass.types.wrapped import WrappedArgFabricABC
from ass.i18n import lazy_gettext as l_


class OptionalArg(WrappedArgFabricABC):

    @property
    def needed_type(self) -> Tuple[LazyProxy, LazyProxy]:
        return (
            l_("Optional {}").format(self.child_fabric.needed_type[0]),
            l_("Optionals {}").format(self.child_fabric.needed_type[0]),
        )

    def check(self, text: str) -> bool:
        return True

    def parse(self, text: str) -> Tuple[Optional[int], Any]:
        if self.child_fabric.check(text):
            with contextlib.suppress(ArgTypeError):
                arg = self.child_fabric(text, 0)
                return arg.length, arg.value
        return 0, None


class OrArg(ArgFabric):
    args_type: Tuple[ArgFabric, ...]

    def __init__(self, *args_type: ArgFabric):
        super().__init__(args_type[0].description)
        self.args_type = args_type

    @property
    def needed_type(self) -> Tuple[LazyProxy, LazyProxy]:
        return (l_(" or ").join(f"'{arg.needed_type[0]}'" for arg in self.args_type),
                l_(" or ").join(f"'{arg.needed_type[1]}'" for arg in self.args_type))

    @staticmethod
    def check(text: str) -> bool:
        return bool(text)

    def pre_parse(self, _text: str, **data) -> Tuple[int, Any]:
        for arg_fabric in self.args_type:
            try:
                text = data.get(
                    'known_end_arg_text' if arg_fabric.know_the_end is True else 'not_known_end_arg_text') or _text

                if not arg_fabric.check(text):
                    continue
                self.know_the_end = arg_fabric.know_the_end

                arg = arg_fabric(text, 0)

                return arg.length or 0, arg.value
            except ArgTypeError:
                continue

        raise ArgTypeError(text=_text, needed_type=self.needed_type, description=self.description)

    def __repr__(self):
        return f'<{self.__class__.__name__}>: {", ".join(str(x) for x in self.args_type)}'
