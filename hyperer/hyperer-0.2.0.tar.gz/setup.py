# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hyperer']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['hyperer-cargo = hyperer.cargo:main',
                     'hyperer-rg = hyperer.rg:main']}

setup_kwargs = {
    'name': 'hyperer',
    'version': '0.2.0',
    'description': '',
    'long_description': 'None',
    'author': 'Charlie Groves',
    'author_email': 'c@sevorg.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
