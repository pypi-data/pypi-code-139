# This “setup.py” file is for the creation of a library:
# It will indicate to Pypi (the Python Package Index) the version of my "nurdalib" library,
# and other metadata for its referencing.

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="nurdalib",
    version="0.1.0",
    description="Homework 1 library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://engineering.nyu.edu/",
    author="Nurdaulet Kaldanov",
    author_email="nk3194@nyu.edu",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["nurdalib"],
    include_package_data=True,
    install_requires=["polygon-api-client==0.2.11"]
)