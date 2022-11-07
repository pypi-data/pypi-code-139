# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['govee_lan_api']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'govee-lan-api',
    'version': '0.1.1a0',
    'description': 'Implementation of the Govee LAN API to control supported Govee products',
    'long_description': "# Govee LAN API Client \n\nThis is a simple API client for [Govee's LAN UDP API](https://app-h5.govee.com/user-manual/wlan-guide)\n",
    'author': 'Ryan McDonough',
    'author_email': 'Ryan@r2n.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
