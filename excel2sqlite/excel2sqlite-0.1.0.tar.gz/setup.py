# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['excel2sqlite']

package_data = \
{'': ['*']}

install_requires = \
['openpyxl>=3.0.10,<4.0.0', 'pandas>=1.5.1,<2.0.0', 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['excel2sqlite = excel2sqlite.cli:app']}

setup_kwargs = {
    'name': 'excel2sqlite',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'CD Clark III',
    'author_email': 'clifton.clark@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
