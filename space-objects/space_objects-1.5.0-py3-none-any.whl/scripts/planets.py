import sys

import click

from space_objects.models import PlanetObserver


@click.group(help="planets subcommands.")
def planets():
    pass


@click.command("get-position", help="get the planet position")
@click.option("--name", prompt="planet name", help="The planet name.")
def position(name):
    if name.upper() not in PlanetObserver.planets_names:
        print(f"ERROR: planet with name < {name} > is not provided.")
        sys.exit(1)
    PlanetObserver(
        observation_position_longitude=0.0,
        observation_position_latitude=0.0,
    ).get_position(name.upper()).tprint()


@click.command("search", help="search if the planet name is provided")
@click.option(
    "--name",
    default="*",
    prompt="planet name contains",
    help="The list of planets where the name contains search.",
)
def search(name):
    name = "" if name == "*" else name.upper()
    planets = PlanetObserver.planets_names
    if name:
        for sname in planets:
            if name in sname:
                print(sname)
    else:
        for sname in planets:
            print(sname)


planets.add_command(position)
planets.add_command(search)
