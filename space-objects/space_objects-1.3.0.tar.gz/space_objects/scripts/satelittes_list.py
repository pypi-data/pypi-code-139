import click

from space_objects.models import TLEFileSatelliteActive


@click.command()
@click.option(
    "--search",
    default="*",
    prompt="satellite name contains",
    help="The list of satellites where the name contains search.",
)
def run(search):
    search = "" if search == "*" else search.upper()
    tlesat = TLEFileSatelliteActive()
    if search:
        for sname in tlesat.list():
            if search in sname:
                print(sname)
    else:
        for sname in tlesat.list():
            print(sname)
