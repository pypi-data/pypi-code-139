# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiotinyrpc',
 'aiotinyrpc.dispatch',
 'aiotinyrpc.protocols',
 'aiotinyrpc.server',
 'aiotinyrpc.transports']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aiotinyrpc',
    'version': '0.1.0',
    'description': '"An aio version of tinyrpc"',
    'long_description': None,
    'author': 'David White',
    'author_email': 'dr.white.nz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
