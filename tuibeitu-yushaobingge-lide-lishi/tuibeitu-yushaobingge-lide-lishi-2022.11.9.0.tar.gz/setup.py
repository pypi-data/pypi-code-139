#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import TuibeituYushaobinggeLideLishi
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('TuibeituYushaobinggeLideLishi'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="tuibeitu-yushaobingge-lide-lishi",
    version=TuibeituYushaobinggeLideLishi.__version__,
    url="https://github.com/apachecn/tuibeitu-yushaobingge-lide-lishi",
    author=TuibeituYushaobinggeLideLishi.__author__,
    author_email=TuibeituYushaobinggeLideLishi.__email__,
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
    description="推背图与烧饼歌里的历史",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "tuibeitu-yushaobingge-lide-lishi=TuibeituYushaobinggeLideLishi.__main__:main",
            "TuibeituYushaobinggeLideLishi=TuibeituYushaobinggeLideLishi.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
