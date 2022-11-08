from setuptools import setup
from pathlib import Path

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="random_number_list",
    version="0.0.1",
    description="To return a list of randomly drawn numbers from a user defined list of numbers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Natural Language :: English",
        "Topic :: Utilities"
    ]
)
