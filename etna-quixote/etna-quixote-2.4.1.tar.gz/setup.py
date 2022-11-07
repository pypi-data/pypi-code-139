# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quixote', 'quixote.build', 'quixote.fetch', 'quixote.inspection']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.29,<4.0.0',
 'etna-api>=3.0.0,<4.0.0',
 'requests>=2.28.0,<3.0.0']

setup_kwargs = {
    'name': 'etna-quixote',
    'version': '2.4.1',
    'description': 'Front-end to write automated tests for Etna projects',
    'long_description': None,
    'author': 'Clément "Doom" Doumergue',
    'author_email': 'clement.doumergue@etna.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
