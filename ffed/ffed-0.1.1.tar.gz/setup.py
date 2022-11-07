# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ffed',
 'ffed.encoders_decoders',
 'ffed.encoders_decoders.tests',
 'ffed.hashes',
 'ffed.hashes.tests']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0']

entry_points = \
{'console_scripts': ['ffed = ffed.main:cli']}

setup_kwargs = {
    'name': 'ffed',
    'version': '0.1.1',
    'description': 'A full-fledged encoder decoder',
    'long_description': '# ffed (full-fledged encoder decoder)\n\n## Installation\n\n```shell\npip install ffed\n```\n\n## Usage\n\n```shell\n# To get the help section\nffed --help\n\n# To get the help section of specific sub command\nffed encode --help\n```\n',
    'author': 'Sahil Rawat',
    'author_email': 'sahil.rawat.1603@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
