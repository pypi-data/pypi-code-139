from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message
from stfu_tg import Section

from ass.exceptions import ARGS_EXCEPTIONS, ArgError
from ass.types.base_abc import ArgFabric, ParsedArg

from ass.i18n import gettext as _
from ass.i18n import gettext_ctx


class ArgsMiddleware(BaseMiddleware):

    @staticmethod
    async def parse_args(text: str, args: Dict[str, ArgFabric]) -> Dict[str, ParsedArg]:
        args_data = {}

        offset = 0

        for arg_codename, arg_fabric in args.items():
            # Strip text and count offset
            offset += (arg_stripped_offset := (len(text) - len(text := text.lstrip())))

            args_data[arg_codename] = (arg := arg_fabric(text, offset))

            offset += arg.length or 0
            text = text[arg.length or 0 + arg_stripped_offset:]

            if not arg.length and text:
                # Argument has no length, and no text left - Means this argument consumes all text
                break

        return args_data

    @staticmethod
    async def send_error(message: Message, error: ArgError):

        doc = Section(
            *error.doc,
            title=_("Argument validation error"),
        )

        await message.answer(str(doc))

    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], message: Message,
                       data: Dict[str, Any]) -> Any:

        if args := get_flag(data, "args"):
            if text := data['command'].args:
                try:
                    data['args'] = await self.parse_args(text, args)
                except ARGS_EXCEPTIONS as e:
                    with data['i18n'].context():
                        gettext_ctx.set(data['i18n'])
                        await self.send_error(message, e)
                    return

        return await handler(message, data)
