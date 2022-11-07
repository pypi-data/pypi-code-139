#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import DakaiAkaxiJiludeYaoshi
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('DakaiAkaxiJiludeYaoshi'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="dakai-akaxi-jilude-yaoshi",
    version=DakaiAkaxiJiludeYaoshi.__version__,
    url="https://github.com/apachecn/dakai-akaxi-jilude-yaoshi",
    author=DakaiAkaxiJiludeYaoshi.__author__,
    author_email=DakaiAkaxiJiludeYaoshi.__email__,
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
    description="打开阿卡西纪录的钥匙",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "dakai-akaxi-jilude-yaoshi=DakaiAkaxiJiludeYaoshi.__main__:main",
            "DakaiAkaxiJiludeYaoshi=DakaiAkaxiJiludeYaoshi.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
