# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cryptologging', 'cryptologging.algorithms']

package_data = \
{'': ['*']}

install_requires = \
['orjson>=3.8.0,<4.0.0']

setup_kwargs = {
    'name': 'cryptologging',
    'version': '0.1.0',
    'description': 'Log encryption',
    'long_description': None,
    'author': 'Cheldaev Alexey',
    'author_email': 'alexothers35@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
