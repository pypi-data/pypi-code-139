"""
Script to download TLE files and de421.bsp file.
"""
import click

from space_objects.models import TLEFileSatelliteActive, TLEFileWeather


@click.command(help="load TLE and de421.bsp files.")
def load_tle():
    TLEFileSatelliteActive()
    TLEFileWeather()
