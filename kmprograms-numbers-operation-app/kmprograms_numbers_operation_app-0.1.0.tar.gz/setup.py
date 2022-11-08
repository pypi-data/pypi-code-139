# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kmprograms_numbers_operation_app',
 'kmprograms_numbers_operation_app.operation']

package_data = \
{'': ['*']}

install_requires = \
['pytz>=2022.6,<2023.0']

setup_kwargs = {
    'name': 'kmprograms-numbers-operation-app',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Krzysztof',
    'author_email': 'programowanie.krzysiek@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
