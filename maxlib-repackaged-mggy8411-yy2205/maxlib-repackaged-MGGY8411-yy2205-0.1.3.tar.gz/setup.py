from setuptools import setup

from codecs import open
from os import path

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="maxlib-repackaged-MGGY8411-yy2205",
    version="0.1.3",
    description="Max's code repackaged as a library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Yue",
    author_email="yy2205@nyu.edu",
    packages=["maxlib"],
    include_package_data=True,
    install_requires=[
        "wheel",
        "pandas",
        "matplotlib",
        "numpy",
        "sqlalchemy",
        "jupyter",
        "polygon-api-client",
    ],
)
