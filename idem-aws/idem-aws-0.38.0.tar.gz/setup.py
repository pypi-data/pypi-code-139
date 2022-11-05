#!/usr/bin/env python3
import os
import pathlib
import shutil

from setuptools import Command
from setuptools import setup

NAME = "idem_aws"
DESC = "AWS Cloud Provider for Idem"

# Version info -- read without importing
_locals = {}
with pathlib.Path(NAME, "version.py").open() as fp:
    exec(fp.read(), None, _locals)

VERSION = _locals["version"]
SETUP_DIRNAME = os.path.dirname(__file__)
if not SETUP_DIRNAME:
    SETUP_DIRNAME = os.getcwd()

with open("README.rst", encoding="utf-8") as f:
    LONG_DESC = f.read()

with pathlib.Path("requirements", "base.txt").open("r") as f:
    REQUIREMENTS = f.read().splitlines()

REQUIREMENTS_EXTRA = {}
EXTRA_PATH = pathlib.Path("requirements", "extra")
if EXTRA_PATH.exists():
    REQUIREMENTS_EXTRA["full"] = set()
    for extra in EXTRA_PATH.iterdir():
        with extra.open("r") as f:
            REQUIREMENTS_EXTRA[extra.stem] = f.read().splitlines()
            REQUIREMENTS_EXTRA["full"].update(REQUIREMENTS_EXTRA[extra.stem])


class Clean(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for subdir in (NAME, "tests"):
            for root, dirs, files in os.walk(
                os.path.join(os.path.dirname(__file__), subdir)
            ):
                for dir_ in dirs:
                    if dir_ == "__pycache__":
                        shutil.rmtree(os.path.join(root, dir_))


def discover_packages():
    modules = []
    for package in (NAME,):
        for root, _, files in os.walk(os.path.join(SETUP_DIRNAME, package)):
            pdir = os.path.relpath(root, SETUP_DIRNAME)
            if "{{cookiecutter.root_dir}}" in pdir or "aws_auto" in pdir:
                continue
            modname = pdir.replace(os.sep, ".")
            modules.append(modname)
    return modules


setup(
    name="idem-aws",
    author="VMware, Inc.",
    author_email="idemproject@vmware.com",
    url="https://docs.idemproject.io/idem-aws/en/latest/index.html",
    project_urls={
        "Code": "https://gitlab.com/vmware/idem/idem-aws",
        "Issue tracker": "https://gitlab.com/vmware/idem/idem-aws/issues",
    },
    version=VERSION,
    install_requires=REQUIREMENTS,
    extras_require=REQUIREMENTS_EXTRA,
    description=DESC,
    long_description=LONG_DESC,
    long_description_content_type="text/x-rst",
    python_requires=">=3.7",
    license="Apache Software License 2.0",
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
    ],
    packages=discover_packages(),
    cmdclass={"clean": Clean},
)
