# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['paas_service',
 'paas_service.auth',
 'paas_service.management',
 'paas_service.management.commands',
 'paas_service.migrations']

package_data = \
{'': ['*']}

install_requires = \
['blue-krill>=1.0.15',
 'django-translated-fields',
 'jsonfield',
 'pyjwt>=1.6.4,<2.0.0']

setup_kwargs = {
    'name': 'paas-service',
    'version': '1.1.4',
    'description': '',
    'long_description': None,
    'author': 'blueking',
    'author_email': 'blueking@tencent.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<3.11',
}


setup(**setup_kwargs)
