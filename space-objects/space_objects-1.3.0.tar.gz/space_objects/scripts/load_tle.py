"""
Script to download TLE files and de421.bsp file.
"""
from space_objects.models import TLEFileSatelliteActive, TLEFileWeather


def run():
    TLEFileSatelliteActive()
    TLEFileWeather()
