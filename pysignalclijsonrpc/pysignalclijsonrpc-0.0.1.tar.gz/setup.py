# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysignalclijsonrpc']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0', 'uuid>=1.30,<2.0']

setup_kwargs = {
    'name': 'pysignalclijsonrpc',
    'version': '0.0.1',
    'description': 'Python API client for signal-cli JSON-RPC',
    'long_description': '# pysignalclijsonrpc - Python API client for signal-cli JSON-RPC\n',
    'author': 'Stefan Heitmüller',
    'author_email': 'stefan.heitmueller@gmx.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
