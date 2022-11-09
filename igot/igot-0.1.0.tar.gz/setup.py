#!/usr/bin/env python3

PROJ_NAME = 'igot'
PACKAGE_NAME = 'i_got'

PROJ_METADATA = '%s.json' % PROJ_NAME

import os, json
here = os.path.abspath(os.path.dirname(__file__))
proj_info = json.loads(open(os.path.join(here, PROJ_METADATA), encoding='utf-8').read())
try:
    README = open(os.path.join(here, 'README.rst'), encoding='utf-8').read()
except:
    README = ""

VERSION = {}
ver_path = os.path.join(here, 'src/%s/version.py' % PACKAGE_NAME)
with open(ver_path, encoding='utf-8') as ver_file:
    exec(ver_file.read(), VERSION)


from setuptools import setup, find_packages
setup(
    name = proj_info['name'],
    version = VERSION['__version__'],

    author = proj_info['author'],
    author_email = proj_info['author_email'],
    url = proj_info['url'],
    license = proj_info['license'],

    description = proj_info['description'],
    keywords = proj_info['keywords'],

    long_description = README,

    packages = find_packages('src'),
    package_dir = {'' : 'src'},

    test_suite = 'tests',

    platforms = 'any',
    zip_safe = True,
    include_package_data = True,

    classifiers = proj_info['classifiers'],

    entry_points = {'console_scripts': proj_info['console_scripts']},

    extras_require={
        'socks': ['PySocks'],
    }
)
