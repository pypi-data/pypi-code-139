# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['transportlib']

package_data = \
{'': ['*']}

install_requires = \
['psycopg2>=2.9.5,<3.0.0']

setup_kwargs = {
    'name': 'transportlib',
    'version': '0.1.1',
    'description': 'Transports for Data Pipelines',
    'long_description': None,
    'author': 'ken ho',
    'author_email': 'kenho811job@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kenho811/flux_infra',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
