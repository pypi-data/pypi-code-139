from setuptools import setup

exec(open("climex/_version.py").read())

setup(
    version=__version__)