# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mava']

package_data = \
{'': ['*']}

install_requires = \
['argon2-cffi>=21.3.0,<22.0.0']

setup_kwargs = {
    'name': 'mava',
    'version': '0.1.2',
    'description': 'A python dataclass library, that can work as an ORM/ODM',
    'long_description': "## MAVA\nA simple dataclass like model, that can be adapted for multiple purposes. It can be used pretty easily with any DB and become an ORM/ODM.\n# Local installation\nRun `./install.sh`.\n\n## Notes\nModels cannot have attributes that start with '_' or with a capital letter.\n",
    'author': 'warevil',
    'author_email': 'jg@warevil.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/warevil/mava',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
