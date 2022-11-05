#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import ZhongguoGongzuofangChuandao
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('ZhongguoGongzuofangChuandao'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="zhongguo-gongzuofang-chuandao",
    version=ZhongguoGongzuofangChuandao.__version__,
    url="https://github.com/apachecn/zhongguo-gongzuofang-chuandao",
    author=ZhongguoGongzuofangChuandao.__author__,
    author_email=ZhongguoGongzuofangChuandao.__email__,
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
    description="中国工作坊传导",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "zhongguo-gongzuofang-chuandao=ZhongguoGongzuofangChuandao.__main__:main",
            "ZhongguoGongzuofangChuandao=ZhongguoGongzuofangChuandao.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
