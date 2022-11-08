# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drivers',
 'drivers.agiltron',
 'drivers.agiltron.ffsw',
 'drivers.arduino.arduino_gpio',
 'drivers.beaglebone',
 'drivers.beaglebone.beaglebone_gpio',
 'drivers.beaglebone.beaglebone_gpio.beaglebone_server',
 'drivers.thorlabs',
 'drivers.thorlabs.cld1010']

package_data = \
{'': ['*'], 'drivers.arduino.arduino_gpio': ['pin_server/*']}

install_requires = \
['pyvisa']

setup_kwargs = {
    'name': 'nspyre-drivers',
    'version': '0.1.0',
    'description': 'A set of Python drivers for lab instrumentation.',
    'long_description': '# drivers\nA set of Python drivers for lab instrumentation. These drivers are associated \nwith [nspyre](https://nspyre.readthedocs.io/en/latest/), but are also suitable \nfor general usage.\n\nIf you want to contribute driver code, please submit it as a \n[pull request](http://TODO). ',
    'author': 'Jacob Feder',
    'author_email': 'jacobsfeder@gmail.com',
    'maintainer': 'Jacob Feder',
    'maintainer_email': 'jacobsfeder@gmail.com',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
