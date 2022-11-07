#!/usr/bin/env python

import io
import os
import re
from setuptools import setup


def read(*names, **kwargs):
    try:
        with io.open(
            os.path.join(os.path.dirname(__file__), *names),
            encoding=kwargs.get("encoding", "utf8")
        ) as fp:
            return fp.read()
    except IOError:
        return ''


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


long_description = read('README.md')


setup(
    name="py_ballisticcalc-stubs",
    url="https://github.com/o-murphy/py_ballisticcalc-stubs",
    author="o-murphy",
    author_email="thehelixpg@gmail.com",
    maintainer="o-murphy",
    maintainer_email="thehelixpg@gmail.com",
    description="PEP561 stub files for the py_ballisticcalc library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=find_version('py_ballisticcalc-stubs', '__init__.pyi'),
    python_requires=">= 3.9",
    package_data={
        "py_ballisticcalc-stubs": ['*.pyi'],
        "py_ballisticcalc-stubs.bmath": ['*.pyi'],
        "py_ballisticcalc-stubs.bmath.vector": ['*.pyi'],
        "py_ballisticcalc-stubs.bmath.unit": ['*.pyi'],
    },
    packages=[
        "py_ballisticcalc-stubs",
        "py_ballisticcalc-stubs.bmath",
        "py_ballisticcalc-stubs.bmath.vector",
        "py_ballisticcalc-stubs.bmath.unit"
    ],
    # extras_require={
    #     "dev": ["mypy==0.930", "pytest", "pytest-xvfb"],
    # },
    # classifiers=[
    #     "Development Status :: 5 - Production/Stable",
    #     "Intended Audience :: Developers",
    #     "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    #     "Programming Language :: Python :: 3",
    #     "Topic :: Software Development"
    # ]
)