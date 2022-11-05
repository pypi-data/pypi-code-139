# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sfdevtools', 'sfdevtools.app', 'sfdevtools.observability']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sfdevtools',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'SulfredLee',
    'author_email': 'sflee1112@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
