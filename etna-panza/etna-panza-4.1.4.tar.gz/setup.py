# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['panza', 'panza.backends', 'panza.internals']

package_data = \
{'': ['*']}

install_requires = \
['etna-quixote>=2.0.0,<3.0.0']

entry_points = \
{'console_scripts': ['panza_executor = panza.executor:main']}

setup_kwargs = {
    'name': 'etna-panza',
    'version': '4.1.4',
    'description': 'Library to manage environments and jobs based on Quixote blueprints',
    'long_description': None,
    'author': 'Clément "Doom" Doumergue',
    'author_email': 'clement.doumergue@etna.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
