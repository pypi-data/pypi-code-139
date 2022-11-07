# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pydo', 'pydo.aio', 'pydo.aio.operations', 'pydo.operations']

package_data = \
{'': ['*']}

install_requires = \
['azure-core>=1.24.0',
 'azure-identity>=1.5.0',
 'isodate>=0.6.1',
 'msrest>=0.7.1',
 'typing-extensions>=3.7.4']

extras_require = \
{'aio': ['aiohttp>=3.0']}

setup_kwargs = {
    'name': 'pydo',
    'version': '0.1.2',
    'description': 'The official client for interacting with the DigitalOcean API',
    'long_description': None,
    'author': 'API Engineering',
    'author_email': 'api-engineering@digitalocean.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
