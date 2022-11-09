# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autobot', 'autobot.core', 'autobot.types', 'autobot.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiogram>=3.0.0b5,<4.0.0',
 'loguru>=0.6.0,<0.7.0',
 'networkx>=2.8.8,<3.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'pyyaml>=6.0,<7.0',
 'tomli>=2.0.1,<3.0.0',
 'uvloop>=0.17.0,<0.18.0']

entry_points = \
{'console_scripts': ['autobot = autobot.__main__:main']}

setup_kwargs = {
    'name': 'autobot-tg',
    'version': '0.1.2a1',
    'description': 'Telegram Bot creation made easy',
    'long_description': '<p align="center">\n    <img src="https://github.com/andrewsapw/autobot/raw/master/docs/static/autobot_head.png" alt="Pyrogram" width="128">\n    <br>\n    <b>AUTOBOT</b>\n    <br>\n</p>\n\n\nFramework for making bot from config files (we all love *YAML*, does\'t we?)\n\n1. [Features](#features)\n2. [Usage](#usage)\n\n# Features\n- **Automatic back button configuration** - not need to plainly think about branching\n- **Beautiful inline buttons experience** - previous message gets updated on button pressed (much cleaner message history)\n- **RegEx message filters**\n\n# Installation\n\n\n# Usage\n\n```sh\nautobot examples/configs/simple.yaml\n```\n\n## Config examples\n- [Simple one](/examples/configs/simple.yaml)\n- [Inline buttons](/examples/configs/inline_buttons.yaml)\n',
    'author': 'Andrew S.',
    'author_email': 'andrewsapw@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/andrewsapw/autobot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
