import sys

import click

from space_objects.models import SatelliteActive, TLEFileSatelliteActive


@click.group(help="satellites subcommands.")
def satellites():
    pass


@click.command("get-position", help="get the satellite position")
@click.option("--name", prompt="satellite name", help="The satellite name.")
def position(name):
    tlesat = TLEFileSatelliteActive()
    if name.upper() not in tlesat.list():
        print(f"ERROR: satellite with name < {name} > is not provided.")
        sys.exit(1)
    SatelliteActive(name.upper()).get_position().tprint()


@click.command("search", help="search if the satellite name is provided")
@click.option(
    "--name",
    default="*",
    prompt="satellite name contains",
    help="The list of satellites where the name contains search.",
)
def search(name):
    name = "" if name == "*" else name.upper()
    tlesat = TLEFileSatelliteActive()
    if name:
        for sname in tlesat.list():
            if name in sname:
                print(sname)
    else:
        for sname in tlesat.list():
            print(sname)


satellites.add_command(position)
satellites.add_command(search)
