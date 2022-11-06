# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['casher']
install_requires = \
['toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'casher',
    'version': '0.5.0',
    'description': 'Module for creating cache files, folders and etc',
    'long_description': '\n# Casher - in development\n\n1. [License](LICENSE.rst)\n\nPython small module for creating cache files, folders and etc. Main purpose is to save data from\nclass, dict, object to local file and fast load it when required.\n\nPrimary usage is wrapping functions and classes for creating cache files.\n',
    'author': 'assertionLimit',
    'author_email': 'markushasorokin@yandex.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
