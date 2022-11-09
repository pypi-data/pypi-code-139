# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lambda_handler', 'lambda_handler.model']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['pydantic>=1.10.2,<2.0.0']

setup_kwargs = {
    'name': 'lambda-handler',
    'version': '0.1.0',
    'description': 'A Python package for routing and validating AWS events inside a Lambda function',
    'long_description': None,
    'author': 'Matthew Badger',
    'author_email': 'matt@branchenergy.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
