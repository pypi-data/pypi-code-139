#!/usr/bin/env python3

import chiaki as project

from setuptools import setup, find_packages
import os


def here(*path):
    return os.path.join(os.path.dirname(__file__), *path)


def get_file_contents(filename):
    with open(here(filename), "r", encoding="utf8") as fp:
        return fp.read()


setup(
    name=project.__name__,
    description=project.__doc__.strip(),
    long_description=get_file_contents("README.md"),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/nul.one/" + project.__name__,
    download_url="https://gitlab.com/nul.one/{1}/-/archive/{0}/{1}-{0}.tar.gz".format(
        project.__version__, project.__name__
    ),
    version=project.__version__,
    author=project.__author__,
    author_email=project.__author_email__,
    license=project.__license__,
    packages=[project.__name__],
    entry_points={
        "console_scripts": [
            "{0}={0}.__main__:cli".format(project.__name__),
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Information Technology",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Communications :: Chat",
    ],
    install_requires=[
        "click-aliases>=1.0.1<1.1",
        "click>=8.1.3<9",
        "googletrans==4.0.0rc1",
        "prompt-toolkit>=3.0.32<4",
    ],
    python_requires=">=3.10",
)
