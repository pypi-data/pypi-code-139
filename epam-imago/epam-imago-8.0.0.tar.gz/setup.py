from setuptools import setup, find_packages
import codecs
import os
import atexit
import sys


VERSION = '8.0.0'
DESCRIPTION = 'hey'
LONG_DESCRIPTION = 'A package that allows to build simple streams ofvideo, audio and camera data.'

# Setting up
setup(
    name="epam-imago",
    version=VERSION,
    author="NeuralNine (Florian Dedov)",
    author_email="<mail@neuralnine.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
