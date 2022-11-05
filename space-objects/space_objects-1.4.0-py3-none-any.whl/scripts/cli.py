import click

from .load_tle import load_tle
from .planets import planets
from .satellites import satellites


@click.group()
def cli():
    pass


cli.add_command(load_tle)
cli.add_command(planets)
cli.add_command(satellites)
