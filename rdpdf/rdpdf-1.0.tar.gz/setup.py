import setuptools
from pathlib import Path

setuptools.setup(
    name="rdpdf",  # project name in repository must be unique
    version=1.0,
    long_description=Path("README.md").read_text(),
    # packages that will be excluded - tests and data folders
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
