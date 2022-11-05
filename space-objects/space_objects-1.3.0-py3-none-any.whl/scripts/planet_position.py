import sys

import click

from space_objects.models import PlanetObserver


@click.command()
@click.option("--name", prompt="planet name", help="The planet name.")
def run(name):
    if name.upper() not in PlanetObserver.planets_names:
        print(f"ERROR: planet with name < {name} > is not provided.")
        sys.exit(1)
    PlanetObserver(
        observation_position_longitude=0.0,
        observation_position_latitude=0.0,
    ).get_position(name.upper()).tprint()
