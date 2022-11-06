#!/usr/bin/env python3
from setuptools import setup
from torxtools.misctools import get_package_requirements

requirements = get_package_requirements()

setup(
    install_requires=requirements,
)
