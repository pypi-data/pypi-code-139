# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_apis', 'python_apis.ad_api', 'python_apis.ad_api.models']

package_data = \
{'': ['*']}

install_requires = \
['dacite>=1.6.0,<2.0.0', 'ldap3>=2.9.1,<3.0.0']

setup_kwargs = {
    'name': 'python-apis',
    'version': '0.1.0',
    'description': 'A package that contains a small collection of easy to use API to common services',
    'long_description': "# Python-APIs\nA collection of easy to use API's that are mostly used for collecting data.\n\nDeveloping Python-APIs\nAlong with the tools you need to develop and run tests, run the following in your virtual env:\npip install -e .[dev]\n",
    'author': 'Björn Gunnarsson',
    'author_email': 'bjorngun@kopavogur.is',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Kopavogur/Python-APIs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
