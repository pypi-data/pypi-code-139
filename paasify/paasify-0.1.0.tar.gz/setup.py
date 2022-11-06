# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'cafram'}

packages = \
['cafram', 'paasify']

package_data = \
{'': ['*'], 'paasify': ['assets/*', 'assets/plugins/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'anyconfig>=0.13.0,<0.14.0',
 'giturlparse>=0.10.0,<0.11.0',
 'jsonnet>=0.18.0,<0.19.0',
 'jsonschema>=4.16.0,<5.0.0',
 'oschmod>=0.3.12,<0.4.0',
 'pydantic>=1.10.2,<2.0.0',
 'ruamel.yaml>=0.17.21,<0.18.0',
 'semver>=2.13.0,<3.0.0',
 'sh>=1.14.3,<2.0.0',
 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['paasify = paasify.cli:app']}

setup_kwargs = {
    'name': 'paasify',
    'version': '0.1.0',
    'description': 'Paasify your docker-compose files',
    'long_description': 'None',
    'author': 'MrJK',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
