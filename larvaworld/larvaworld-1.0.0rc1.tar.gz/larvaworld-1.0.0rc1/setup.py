from setuptools import setup, find_packages
import os
import sys

name='larvaworld'

if sys.version_info[0] < 3:
    with open('README.md') as f:
        long_description = f.read()
else:
    with open('README.md', encoding='utf-8') as f:
        long_description = f.read()

setup(
    name=name,
    version='1.0.0-rc-1',
    description='Drosophila larva behavioral analysis and simulation platform',
    long_description_content_type='text/markdown',
    long_description=long_description,
    author='Panagiotis Sakagiannis',
    author_email='bagjohn0@gmail.com',
    url='https://github.com/nawrotlab/larvaworld',
    license='MPL-2.0',
    packages=find_packages(),
    #install_requires=[
    #    'click==6.7',
    #    'numpy==1.13.1',
    #    'pyyaml==3.12',
    #],
    scripts=['bin/larvaworld', 'bin/larvaworld_gui'],
    include_package_data=True,
    classifiers=[
        #'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.9',
    ],
)
