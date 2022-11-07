# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hl7conv']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'hl7conv',
    'version': '0.1.1',
    'description': 'Converts hl7 and json formats in both ways',
    'long_description': 'The project goal is to implement hl7-to-json, json-to-hl7 converter with validation for hl7 popular versions.',
    'author': 'Ilya Kalosha',
    'author_email': 'kalosha.ilya@yandex.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/IlyaKalosha/hl7conv',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10.4,<4.0.0',
}


setup(**setup_kwargs)
