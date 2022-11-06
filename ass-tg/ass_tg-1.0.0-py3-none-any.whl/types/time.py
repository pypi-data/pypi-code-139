import datetime
import re
from typing import Tuple

from babel.support import LazyProxy

from ass.types.oneword import WordArg
from ass.i18n import lazy_gettext as l_

ACTION_TIME_REGEX = re.compile(r"(\d+[ywdhm])")
ACTION_TIME_CHECK_REGEX = re.compile(r"^(\d+[ywdhm])+$")


class ActionTimeArg(WordArg):
    know_the_end = True

    @staticmethod
    def parse_string(text: str) -> int:

        minutes = 0

        for item in ACTION_TIME_REGEX.findall(text):
            if item[-1] == "y":
                minutes += int(item[:-1]) * 60 * 24 * 365
            elif item[-1] == "w":
                minutes += int(item[:-1]) * 60 * 24 * 7
            elif item[-1] == "d":
                minutes += int(item[:-1]) * 60 * 24
            elif item[-1] == "h":
                minutes += int(item[:-1]) * 60
            elif item[-1] == "m":
                minutes += int(item[:-1])
            else:
                raise ValueError("Unknown time unit")

        return minutes

    @property
    def needed_type(self) -> Tuple[LazyProxy, LazyProxy]:
        return l_("Action time"), l_("Action times")

    def value(self, text: str) -> datetime.timedelta:
        return datetime.timedelta(minutes=self.parse_string(text))

    def check_type(self, text: str) -> bool:
        return bool(ACTION_TIME_CHECK_REGEX.match(text))
