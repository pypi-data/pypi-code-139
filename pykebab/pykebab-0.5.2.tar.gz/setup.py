# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kebab', 'kebab.cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'deprecation>=2.1.0,<3.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'pyyaml>=6.0,<7.0']

extras_require = \
{'aws': ['boto3>=1.26.3,<2.0.0'], 'k8s': ['kubernetes>=25.3.0,<26.0.0']}

entry_points = \
{'console_scripts': ['kebab = kebab.cli:run']}

setup_kwargs = {
    'name': 'pykebab',
    'version': '0.5.2',
    'description': '',
    'long_description': 'None',
    'author': 'Yangming Huang',
    'author_email': 'leonmax@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
