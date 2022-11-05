# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['workerconnector']

package_data = \
{'': ['*']}

install_requires = \
['celery[redis]>=5.2.7,<6.0.0']

setup_kwargs = {
    'name': 'workerconnector',
    'version': '0.1.0',
    'description': '',
    'long_description': '## coming soon',
    'author': 'redloratech',
    'author_email': 'rede.akbar@loratechai.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
