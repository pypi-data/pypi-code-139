# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['docto']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'docto',
    'version': '0.24.20',
    'description': 'dependancy confusion test',
    'long_description': '# package to test dependacy confusion\n',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
