# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rolos']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rolos',
    'version': '0.1.0',
    'description': 'root project for Rolos python namespace',
    'long_description': '# rolos\nroot project for Rolos python namespace\n',
    'author': 'Andriy Svyetlov',
    'author_email': 'andriy.svyetlov@rolos.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://rolos.com',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
