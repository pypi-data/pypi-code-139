# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kibera', 'kibera.core']

package_data = \
{'': ['*']}

install_requires = \
['flask>=2.2.2,<3.0.0',
 'portforward>=0.3.0,<0.4.0',
 'prometheus-client>=0.15.0,<0.16.0',
 'pymongo>=4.3.2,<5.0.0',
 'redis>=3.5.3,<4.0.0',
 'rich>=12.6.0,<13.0.0',
 'tqdm>=4.60.0,<5.0.0',
 'waitress>=2.1.2,<3.0.0']

entry_points = \
{'console_scripts': ['kibera = kibera:main']}

setup_kwargs = {
    'name': 'kibera',
    'version': '0.1.1',
    'description': '',
    'long_description': 'None',
    'author': 'Hadi',
    'author_email': 'hadi.zolfaghaari@gmail.com',
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
