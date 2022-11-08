#!/usr/bin/env python3
from setuptools import setup
from setuptools import find_packages
from pathlib import Path

setup( 
    name="list_visible_only_dir_content", # This is the name is what you pip install
    version="1.0", # 0.0.number impleys the code isnt stable
    author="Mohamed Shalaby",
    author_email="mshalaby@mail.com",
    description="lists visible only content of a given directory",
    long_description=Path("README.md").read_text(),
    platforms=["Linix,Mac OS"],
    packages=find_packages(exclude=["setup.sh"]),
    py_modules=["ls_vo"],#name of the py file that will be imported
    package_dir={'':'src'}, #maps to src -> srccode
    install_requires=[],

    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    extras_requires= {
        "dev": [
            "pytest>3.7",
        ],
    },   
)