# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aslabs', 'aslabs.dependencies.postgresql']

package_data = \
{'': ['*']}

install_requires = \
['aslabs-dependencies', 'psycopg2>=2.9.3,<3.0.0']

setup_kwargs = {
    'name': 'aslabs-dependencies-postgresql',
    'version': '0.0.2',
    'description': '',
    'long_description': '',
    'author': 'Titusz Ban',
    'author_email': 'tituszban@antisociallabs.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
