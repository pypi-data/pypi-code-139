from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.MD"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.9.0'
DESCRIPTION = 'Software manager useful for installing programs'
LONG_DESCRIPTION = 'Simple Software manager useful for installing programs for the Linux Distros test quickly and automatically, or Simple Installation for Personal configuration'

# Setting up
setup(
    name="software_manager",
    version=VERSION,
    author="C-JeanDev Jean Claude Coppola",
    author_email="<jeanclaudecoppola83@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['getch', 'print_color'],
    keywords=['python', 'software', 'software_manager', 'manager', 'install', ''],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)