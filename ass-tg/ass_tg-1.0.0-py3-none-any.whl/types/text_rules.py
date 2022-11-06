from typing import Any, Tuple

from ass.types.wrapped import WrappedArgFabricABC


class WrappedArgStartsWith(WrappedArgFabricABC):
    starts_with: str

    def __init__(self, starts_with: str, *args):
        super().__init__(*args)

        self.starts_with = starts_with

    def check(self, text: str) -> bool:
        return self.starts_with in text

    def parse(self, text: str) -> Tuple[int, Any]:
        _start, text = text.split(self.starts_with, 1)

        # Strip text and count offset
        arg_stripped_offset = (len(text) - len(text := text.lstrip())) + len(self.starts_with)

        length, data = super().parse(text)
        return length + arg_stripped_offset, data


class UntilArg(WrappedArgFabricABC):
    until_text: str

    # TODO: Description

    def __init__(self, until_text: str, *args):
        super().__init__(*args)

        self.until_text = until_text

    def parse(self, text: str) -> Tuple[int, Any]:
        arg_text = text
        if self.until_text in text:
            arg_text, _rest = text.split(self.until_text, 1)

        length, data = super().parse(arg_text)

        if not length:
            length = len(text)

        return length, data
