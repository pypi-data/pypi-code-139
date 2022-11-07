#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import RentiNengliangZhongxindeZhenxiang
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('RentiNengliangZhongxindeZhenxiang'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="renti-nengliang-zhongxinde-zhenxiang",
    version=RentiNengliangZhongxindeZhenxiang.__version__,
    url="https://github.com/apachecn/renti-nengliang-zhongxinde-zhenxiang",
    author=RentiNengliangZhongxindeZhenxiang.__author__,
    author_email=RentiNengliangZhongxindeZhenxiang.__email__,
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
    description="人体能量中心的真相",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "renti-nengliang-zhongxinde-zhenxiang=RentiNengliangZhongxindeZhenxiang.__main__:main",
            "RentiNengliangZhongxindeZhenxiang=RentiNengliangZhongxindeZhenxiang.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
