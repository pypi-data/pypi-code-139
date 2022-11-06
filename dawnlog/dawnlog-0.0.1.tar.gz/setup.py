# -*- coding:  utf-8 -*-
# @Author:     YLM
# @Time:       2022/11/5 9:32 下午
# @Software:   PyCharm
# @File:       setup.py

from setuptools import setup, find_packages

# read read me
with open("README.txt", "r") as fh:
    long_description = fh.read()

setup(
    name="dawnlog",
    version="0.0.1",
    description="print console log and write logs to file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6.5",
    url="https://github.com/xxxxx",
    author="DawnYang",
    author_email="ylm1392010@qq.com",
    license="MIT Licence",
    install_requires=["colorlog"],
    packages=find_packages(),
    platforms="any",
)
