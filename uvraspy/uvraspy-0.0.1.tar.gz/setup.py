from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

long_description = 'A Python package for Raspberry Pi'

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'A Python package for Raspberry Pi'

# Setting up
setup(
    name="uvraspy",
    version=VERSION,
    author="csM5-22-25",
    author_email="n.aukes@student.utwente.nl",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    keywords=['python', 'RasPy', 'uvedora', 'pihat', 'fedora', ],
    classifiers=[
        
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ]
)


# TODO: add more setup stuff
