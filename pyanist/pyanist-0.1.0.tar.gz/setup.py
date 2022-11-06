# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyanist']

package_data = \
{'': ['*'], 'pyanist': ['dictionaries/*', 'word-frequency-lists/*']}

install_requires = \
['keyboard>=0.13.5,<0.14.0']

setup_kwargs = {
    'name': 'pyanist',
    'version': '0.1.0',
    'description': 'Pyanist allows using chorded typing in addition to normal typing in order to improve your typing speed',
    'long_description': 'None',
    'author': 'Dániel Kántor',
    'author_email': 'git@daniel-kantor.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
