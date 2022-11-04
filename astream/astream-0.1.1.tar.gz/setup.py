# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['astream']

package_data = \
{'': ['*']}

install_requires = \
['wrapt>=1.14.1,<2.0.0']

setup_kwargs = {
    'name': 'astream',
    'version': '0.1.1',
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
