# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eliud',
 'eliud.apps',
 'eliud.commands',
 'eliud.commands.generic',
 'eliud.conf',
 'eliud.conf.locale',
 'eliud.core',
 'eliud.core.bot',
 'eliud.core.checks',
 'eliud.core.checks.security',
 'eliud.core.mail',
 'eliud.core.management',
 'eliud.core.management.commands',
 'eliud.core.serializers',
 'eliud.core.servers',
 'eliud.db',
 'eliud.db.migrations',
 'eliud.dispatch',
 'eliud.markups',
 'eliud.middleware',
 'eliud.template',
 'eliud.template.backends',
 'eliud.test',
 'eliud.utils',
 'eliud.utils.translation']

package_data = \
{'': ['*'],
 'eliud.conf': ['app_template/*',
                'app_template/migrations/*',
                'project_template/*',
                'project_template/apps/*',
                'project_template/project_name/*']}

install_requires = \
['asgiref>=3.5.2,<4.0.0', 'pytz>=2022.6,<2023.0']

entry_points = \
{'console_scripts': ['eliud = eliud.core.management:execute_from_command_line']}

setup_kwargs = {
    'name': 'eliud',
    'version': '0.1.0',
    'description': 'Python Telegram bot Framework',
    'long_description': '# Eliud\n\nA simple Framework to create Telegram Bots (WIP)\n\n[![Tests](https://github.com/ragnarok22/eliud/actions/workflows/tests.yml/badge.svg)](https://github.com/ragnarok22/eliud/actions/workflows/tests.yml)\n[![Docs](https://github.com/ragnarok22/eliud/actions/workflows/publish-docs.yml/badge.svg)](https://github.com/ragnarok22/eliud/actions/workflows/publish-docs.yml)\n![GitHub](https://img.shields.io/github/license/ragnarok22/eliud)\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)\n\n---\n\n**Documentation**: https://ragnarok22.github.io/eliud\n\n**Source Code**: https://github.com/ragnarok22/eliud\n\n---\n\n## Requirements\nPython 3.8+\n\n## Installation\n```shell\n$ pip install eliud\n```\n',
    'author': 'Reinier Hernández',
    'author_email': 'sasuke.reinier@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ragnarok22/eliud',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
