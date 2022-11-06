#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 13:45:49 2022

@author: jiayueli
"""

from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A package to call the polygon api'
LONG_DESCRIPTION = 'A package that repeatedly calls the polygon api every 1 seconds for 24 hours, stores the results, and protects the key information'

setup(
    name="call_polygon_api",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="<Jiayue Li & Max>",
    author_email="<jl12143@nyu.edu>",
    license='MIT',
    packages=find_packages(),
    install_requires=[],
    keywords='api',
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ]
)
