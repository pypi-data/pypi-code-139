# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kthutils']

package_data = \
{'': ['*']}

install_requires = \
['cachetools>=5.2.0,<6.0.0', 'weblogin>=1.0,<2.0']

setup_kwargs = {
    'name': 'kthutils',
    'version': '0.2',
    'description': 'Various tools for automation at KTH',
    'long_description': None,
    'author': 'Daniel Bosk',
    'author_email': 'dbosk@kth.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
