#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import MbaNvwuDainiKaitongNengliang
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('MbaNvwuDainiKaitongNengliang'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="mba-nvwu-daini-kaitong-nengliang",
    version=MbaNvwuDainiKaitongNengliang.__version__,
    url="https://github.com/apachecn/mba-nvwu-daini-kaitong-nengliang",
    author=MbaNvwuDainiKaitongNengliang.__author__,
    author_email=MbaNvwuDainiKaitongNengliang.__email__,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: Other/Proprietary License",
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Text Processing :: Markup :: Markdown",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Documentation",
        "Topic :: Documentation",
    ],
    description="MBA女巫带你开通能量",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "mba-nvwu-daini-kaitong-nengliang=MbaNvwuDainiKaitongNengliang.__main__:main",
            "MbaNvwuDainiKaitongNengliang=MbaNvwuDainiKaitongNengliang.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
