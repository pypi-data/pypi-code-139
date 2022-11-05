# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_priviledge_deescalation']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bapp-aws-priviledge-deescalation',
    'version': '0.0.1',
    'description': 'balcony app for preventing IAM Role & User priviledge escalation by creating customized IAM Permission Boundaries for each of them ',
    'long_description': '# balcony-app-template\nA template repository for creating new Balcony Apps.\n',
    'author': 'Oguzhan Yilmaz',
    'author_email': 'oguzhanylmz271@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
