import click

from swc.version import __version__
from swc.swc_processor import SwcProcessor

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

processor = SwcProcessor()


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(__version__)
def cli():
    """stopwatch command"""


@cli.command()
def start():
    processor.start(2)
