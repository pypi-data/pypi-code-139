# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['personal_logger']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['plog = personal_logger.cli:main']}

setup_kwargs = {
    'name': 'personal-logger',
    'version': '0.1.1',
    'description': '',
    'long_description': '',
    'author': 'Teddy Xinyuan Chen',
    'author_email': '45612704+tddschn@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tddschn/personal-logger',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
