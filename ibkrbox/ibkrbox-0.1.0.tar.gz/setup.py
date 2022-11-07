# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ibkrbox']

package_data = \
{'': ['*']}

install_requires = \
['ib-insync>=0.9.71,<0.10.0']

entry_points = \
{'console_scripts': ['ibkrbox = ibkrbox.cli:cli']}

setup_kwargs = {
    'name': 'ibkrbox',
    'version': '0.1.0',
    'description': 'box spread utility for interactive brokers',
    'long_description': '# ibkrbox\nbox spread utility for interactive brokers\n',
    'author': 'asemx',
    'author_email': '998264+asemx@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/asemx/ibkrbox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
