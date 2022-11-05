# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sfdevtools', 'sfdevtools.app', 'sfdevtools.observability']

package_data = \
{'': ['*']}

install_requires = \
['logging-json>=0.2.1,<0.3.0']

setup_kwargs = {
    'name': 'sfdevtools',
    'version': '0.1.1',
    'description': '',
    'long_description': '',
    'author': 'SulfredLee',
    'author_email': 'sflee1112@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
