from setuptools import setup

with open("README.md", "r") as fh:
    description = fh.read()

setup(
    name="testing_packing",
    version="0.0.2",
    long_description=description,
    long_description_content_type="text/markdown",
    packages=['testing_packing'],
    author="Han Zaw Nyein",
    author_email="hanzawnyineonline@gmail.com",
)