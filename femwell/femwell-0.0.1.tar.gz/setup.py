# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['femwell', 'femwell.tests']

package_data = \
{'': ['*']}

install_requires = \
['scikit-fem @ git+https://github.com/requests/requests.git']

setup_kwargs = {
    'name': 'femwell',
    'version': '0.0.1',
    'description': 'Mode solver for photonic and electric waveguides based on FEM',
    'long_description': 'None',
    'author': 'Helge Gehring',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/HelgeGehring/femwell',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
