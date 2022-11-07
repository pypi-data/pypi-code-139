# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['astream', 'astream.experimental']

package_data = \
{'': ['*']}

install_requires = \
['decorator>=5.1.1,<6.0.0', 'wrapt>=1.14.1,<2.0.0']

setup_kwargs = {
    'name': 'astream',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'Pedro Batista',
    'author_email': 'pedrovhb@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
