# Copyright 2022 Mathias Lechner

from __future__ import absolute_import
from setuptools import setup, find_packages

setup(
    name="canyonrun",
    version="0.0.2",
    packages=find_packages(),  # include/exclude arguments take * as wildcard, . for any sub-package names
    description="Canyon-Run package",
    url="https://github.com/mlech26l/",
    author="Mathias Lechner",
    author_email="mlech26l@gmail.com",
    license="Apache License 2.0",
    install_requires=[
        "packaging",
        "future",
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
    ],
)