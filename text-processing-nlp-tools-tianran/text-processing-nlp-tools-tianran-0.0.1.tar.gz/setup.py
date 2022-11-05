# -*- coding: utf-8 -*-
# @Time    : 11/5/22 3:52 PM
# @Author  : LIANYONGXING
# @FileName: setup.py
# @Software: PyCharm
# @Repo    : https://github.com/lianyongxing/

#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='text-processing-nlp-tools-tianran',
    version='0.0.1',
    author='tianran',
    author_email='512796933@qq.com',
    url='https://github.com/lianyongxing/',
    description=u'文本处理',
    packages=['text-processing-nlp-tools'],
    install_requires=['flashtext', 'jieba-fast', 'tqdm']
)