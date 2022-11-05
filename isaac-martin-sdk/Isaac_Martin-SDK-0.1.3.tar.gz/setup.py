# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['isaac_martin_sdk', 'isaac_martin_sdk.resources']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses-json>=0.5.7,<0.6.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'isaac-martin-sdk',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Isaac Martin',
    'author_email': 'isaac.gregory.martin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
