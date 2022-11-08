# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kmprograms_app_exercises']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'kmprograms-app-exercises',
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
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
