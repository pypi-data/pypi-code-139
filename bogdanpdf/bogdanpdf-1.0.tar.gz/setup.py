import setuptools
from pathlib import Path

setuptools.setup(
    name="bogdanpdf",
    version=1.0,
    long_description=Path("readme.md").read_text(encoding="utf-8"),
    packages=setuptools.find_packages(exclude=["test", "data"])
)
