#!/usr/bin/python3 #
# !coding:utf-8 #
from setuptools import setup, find_packages

setup(
    name="crawl-request",
    version="1.0.1",
    author="znz",
    author_email="zhang_naizhao@163.com",
    description="fast request util.",
    packages=find_packages(),
    install_requires=[
        "cchardet==2.1.7",
        "aiohttp==3.8.3"
    ],
    url="https://cn.bing.com/",
    platforms="any",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],

)
