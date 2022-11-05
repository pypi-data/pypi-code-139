import sys

import click

from space_objects.models import SatelliteActive, TLEFileSatelliteActive


@click.command()
@click.option("--name", prompt="satellite name", help="The satellite name.")
def run(name):
    tlesat = TLEFileSatelliteActive()
    if name.upper() not in tlesat.list():
        print(f"ERROR: satellite with name < {name} > is not provided.")
        sys.exit(1)
    SatelliteActive(name.upper()).get_position().tprint()
