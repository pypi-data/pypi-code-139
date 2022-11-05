#! /usr/bin/env python
#
# Copyright (c) 2020 Alberto Mardegan <mardy@users.sourceforge.net>
#
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.

from setuptools import setup, find_packages

setup(
    name="deride",
    version="0.1",
    description="A generator of mock classes for C/C++ unit testing",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Alberto Mardegan',
    author_email='info@mardy.it',
    url='https://gitlab.com/mardy/deride',
    packages=find_packages(),
    package_data={'deride': ['templates/*.j2']},
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: C',
        'Programming Language :: C++',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Testing :: Unit',
        'Topic :: Utilities',
    ],
    entry_points={
        'console_scripts': [
            'deride=deride.__main__:main',
        ],
    },
    install_requires=[
        'Jinja2',
        'clang',
    ],
    tests_require=[
        'pytest',
    ],
)
