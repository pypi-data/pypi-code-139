# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rediscreen']

package_data = \
{'': ['*']}

install_requires = \
['redis>=4.3.4,<5.0.0', 'textual[dev]>=0.3.0,<0.4.0']

setup_kwargs = {
    'name': 'rediscreen',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Eli Cohen',
    'author_email': 'amihai.cohen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
