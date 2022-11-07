import fnmatch
import logging

BLACK = 0
RED = 196
GREEN = 118
YELLOW = 229
BLUE = 75
MAGENTA = 206
CYAN = 45
WHITE = 255

RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[38;5;%dm"
BOLD_SEQ = "\033[1m"

COLORS = {
    "WARNING": YELLOW,
    "INFO": WHITE,
    "DEBUG": BLUE,
    "CRITICAL": YELLOW,
    "ERROR": RED,
}

# Taken from sentry lib
COMMON_RECORD_ATTRS = frozenset(
    (
        "args",
        "created",
        "exc_info",
        "exc_text",
        "filename",
        "funcName",
        "levelname",
        "levelno",
        "linenno",
        "lineno",
        "message",
        "module",
        "msecs",
        "msg",
        "name",
        "pathname",
        "process",
        "processName",
        "relativeCreated",
        "stack",
        "tags",
        "thread",
        "threadName",
        "stack_info",
        "asctime",
        "color_message",
    )
)


class CustomFormatter(logging.Formatter):
    def __init__(self, fmt, colors=[], colored_levels=True):
        logging.Formatter.__init__(self, fmt)
        self.colors = colors
        self.colored_levels = colored_levels
        self.cache = {}

    def formatMessage(self, record):
        msg = super().formatMessage(record)
        extras = " ".join(
            [
                f"{k}:{record.__dict__[k]}"
                for k in record.__dict__
                if k not in COMMON_RECORD_ATTRS
            ]
        )
        if not extras:
            return msg
        return f"{msg} | {extras}"

    def format(self, record: logging.LogRecord):
        levelname = record.levelname
        if self.colored_levels and levelname in COLORS:
            levelname_color = COLOR_SEQ % COLORS[levelname] + levelname + RESET_SEQ
            record.levelname = levelname_color

        # record.msg = record.name
        color = self.get_color(record.name)

        if color is not None:
            record.msg = COLOR_SEQ % color + record.msg + RESET_SEQ
            record.name = COLOR_SEQ % color + record.name + RESET_SEQ
        return super().format(record)

    def get_color(self, name):
        if name not in self.cache:
            color = None
            for match_with, c in self.colors:
                if fnmatch.fnmatch(name, match_with):
                    color = c
                    break
            self.cache[name] = color
        return self.cache[name]


def init_logging(loglevel=logging.INFO, logfile=None, colors=[], **kwargs):

    fmt = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

    if type(loglevel) is str:
        loglevel = logging.getLevelName(loglevel.upper())

    if logfile:
        handler = logging.FileHandler(logfile)
    else:
        handler = logging.StreamHandler()
    handler.setFormatter(CustomFormatter(fmt, colors))
    handler.setLevel(loglevel)

    logging.basicConfig(
        level=loglevel,
        handlers=[handler],
    )
