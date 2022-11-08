#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
# File: setup.py
# Project: Sloppy
# Created Date: 2022-07-18, 09:28:34
# Author: Chungman Kim(h2noda@unipark.kr)
# Last Modified: Tue Nov 08 2022
# Modified By: Chungman Kim
# Copyright (c) 2022 Unipark
# HISTORY:
# Date      	By	Comments
# ----------	---	----------------------------------------------------------
'''
from glob import glob
from os.path import basename, splitext
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Sloppy",
    version="0.0.0.0.0.0.0.31",
    author="Chungman Kim",
    author_email="h2noda@gmail.com",
    description="Python module - Sloppy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
            "beautifulsoup4",
            "openpyxl",
            "rich",
            "python-dateutil",
            "paramiko",
            "cryptography",
    ],
    url="https://github.com/Cheung-man/Sloppy.git",
    py_modules=["Sloppy/common",
                "Sloppy/error",
                "Sloppy/excel",
                "Sloppy/json",
                "Sloppy/message",
                "Sloppy/database",
                "Sloppy/config",
                "Sloppy/log",
                "Sloppy/remote",
                "Sloppy/database",
                "Sloppy/security",
                "Sloppy/api",
                ],
    python_requires='>=3.9',
)
