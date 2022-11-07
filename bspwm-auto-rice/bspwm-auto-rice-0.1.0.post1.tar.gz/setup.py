# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bspwm_auto_rice']

package_data = \
{'': ['*']}

install_requires = \
['pywal>=3.3.0,<4.0.0', 'rich>=12.6.0,<13.0.0', 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['bspar = bspwm_auto_rice.bspar:cli']}

setup_kwargs = {
    'name': 'bspwm-auto-rice',
    'version': '0.1.0.post1',
    'description': '',
    'long_description': '',
    'author': 'AbdelrhmanNile',
    'author_email': 'abdelrhmannile@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
