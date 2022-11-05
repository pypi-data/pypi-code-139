# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['auto_ricer']

package_data = \
{'': ['*']}

install_requires = \
['pywal>=3.3.0,<4.0.0', 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['auto-ricer = auto_ricer.autoricer:cli']}

setup_kwargs = {
    'name': 'auto-ricer',
    'version': '0.1.2.post5',
    'description': '',
    'long_description': '## auto ricer\nA simple script to automatically rice bspwm, polybar, gtk, and more.',
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
