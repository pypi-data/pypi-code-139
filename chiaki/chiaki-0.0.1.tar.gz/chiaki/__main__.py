"""
chiaki main module.
"""
import chiaki
from chiaki.exceptions import *
from chiaki.translator import Translator
from click_aliases import ClickAliasedGroup
from prompt_toolkit import prompt
import chiaki as app
import click
import logging
import sys

logging.basicConfig()
logger = logging.getLogger("chiaki")
logger.setLevel(logging.WARNING)


class color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"

def keep_translating(source, target):
    text = ""
    tr = Translator(source, target)
    print("Write multiline text. Alt+Return to enter. Enter empty to exit.\n")
    while True:
        text = prompt(
                default=text,
                multiline=True
                )
        if not text:
            return
        target, test = tr.retranslate(text)
        print(f"{color.GREEN}{target}{color.END}")
        print(f"{color.YELLOW}{test}{color.END}")
        

def add_options(options:list):
    "Aggregate click options from a list and pass as single decorator."
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options

_translator_options= [
    click.option('-s', '--source', type=str, show_default=True, default="en",
        help="Language of the source text.",
    ),
    click.option('-t', '--target', type=str, show_default=True, default="ja",
        help="Language of the target text.",
    ),
    ]

@click.group(cls=ClickAliasedGroup)
@click.version_option(
    version=app.__version__, message=f"%(prog)s %(version)s - {app.__copyright__}"
)
@click.option(
    "-d",
    "--debug",
    is_flag=True,
    help="Enable debug mode with output of each action in the log.",
)
@click.pass_context
def cli(ctx, **kwargs):
    if ctx.params.get("debug"):
        logger.setLevel(logging.DEBUG)
        logger.info("debug mode is on")

@cli.command(aliases=["tr"])
@add_options(_translator_options)
@click.argument("text", type=str)
def translate(**kwargs):
    "Translate text from source to target language."
    tr = Translator(source=kwargs["source"], target=kwargs["target"])
    target = tr.translate(
            text = kwargs["text"]
            )
    print(target)

@cli.command(aliases=["rt"])
@add_options(_translator_options)
def retranslate(**kwargs):
    "Translate text from source to target language and back to source."
    keep_translating(source=kwargs["source"], target=kwargs["target"])

if __name__ == "__main__":
    cli()

