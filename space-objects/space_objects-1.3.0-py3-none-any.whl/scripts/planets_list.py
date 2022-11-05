import click

from space_objects.models import PlanetObserver


@click.command()
@click.option(
    "--search",
    default="*",
    prompt="planet name contains",
    help="The list of planets where the name contains search.",
)
def run(search):
    search = "" if search == "*" else search.upper()
    planets = PlanetObserver.planets_names
    if search:
        for sname in planets:
            if search in sname:
                print(sname)
    else:
        for sname in planets:
            print(sname)
