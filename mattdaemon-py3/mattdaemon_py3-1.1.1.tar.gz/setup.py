import os.path

from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="mattdaemon_py3",
    version="1.1.1",
    author="Maurya Allimuthu",
    author_email="catchmaurya@gmail.com",
    description="Easily daemonize your python projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/catchmaurya/mattdaemon_py3",
    packages=find_packages(),
    keywords="daemon daemonize daemonise cli matt",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
