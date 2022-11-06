# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pwpush', 'pwpush.commands']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8.2,<3.0.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.5.1,<13.0.0',
 'shellingham>=1.5.0,<2.0.0',
 'typer[all]>=0.6.1,<0.7.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=4.5.0,<5.0.0']}

entry_points = \
{'console_scripts': ['pwpush = pwpush.__main__:app']}

setup_kwargs = {
    'name': 'pwpush',
    'version': '0.9.0',
    'description': 'Command Line Interface to Password Pusher.',
    'long_description': '# pwpush\n\n<div align="center">\n\n[![Build status](https://github.com/pglombardo/pwpush-cli/workflows/build/badge.svg?branch=master&event=push)](https://github.com/pglombardo/pwpush-cli/actions?query=workflow%3Abuild)\n[![Python Version](https://img.shields.io/pypi/pyversions/pwpush.svg)](https://pypi.org/project/pwpush/)\n[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/pglombardo/pwpush-cli/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)\n[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pglombardo/pwpush-cli/blob/master/.pre-commit-config.yaml)\n[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/pglombardo/pwpush-cli/releases)\n[![License](https://img.shields.io/github/license/pglombardo/pwpush-cli)](https://github.com/pglombardo/pwpush/blob/master/LICENSE)\n\nCommand Line Interface to Password Pusher.\n  \n<strong>This utility is currently in pre-beta form.  Most core functionality exists and works but needs a bit of polishing.</strong>\n\n</div>\n\n# Overview\n\nThis command line utility exists to interface with [pwpush.com](https://pwpush.com) or any privately hosted instance of [Password Pusher](https://github.com/pglombardo/PasswordPusher).\n\nIt uses the JSON API of Password Pusher to create, view, retrieve and manage pushes.  It can do this anonymously or via the authenticated API.\n\n# Installation\n\n`pip install pwpush`\n\n* Required Python version >3.5\n\n# Quickstart\n\n## pwpush.com\n\n```sh\n# Push a password to pwpush.com\n> pwpush push mypassword\nhttps://pwpush.com/en/p/uzij1ybk6rol\n\n# Get JSON output instead\n> pwpush --json=true push mypassword\n{\'url\': \'https://pwpush.com/en/p/uzij1ybk6rol\'}\n```\n## Private Self Hosted Instance\n\n```sh\n# Point this tool to your privately hosted instance\n> pwpush config set --key url --value https://pwpush.mydomain.secure\n# ...and push away...\n> pwpush push mypassword\nhttps://pwpush.mydomain.secure/en/p/uzij1ybk6rol\n```\n\n## Authentication with API Token\n\nGet [the API token associated with your account](https://pwpush.com/en/users/token) and add it to the CLI configuration.\n\n```sh\n# Get your API token at [/en/users/token](https://pwpush.com/en/users/token)\n\n# Configure the CLI with your email and API token\n> pwpush config set --key email --value <pwpush login email>\n> pwpush config set --key token --value <api token from /en/users/token>\n\n# List active pushes in your dashboard\n> pwpush list\n\n=== Active Pushes:\n┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓\n┃ Secret URL Token   ┃ Note                   ┃ Views ┃ Days  ┃ Deletable by Viewer ┃ Retrieval Step ┃ Created                ┃\n┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩\n│ uzij1ybk6rol       │ Push prior to Digital  │ 6/100 │ 28/87 │ True                │ False          │ 10/08/2022, 11:55:49   │\n│                    │ Ocean migration 3      │       │       │                     │                │ UTC                    │\n│ sfoej1fwlfljwlf    │ Push prior to Digital  │ 0/100 │ 28/90 │ True                │ True           │ 10/08/2022, 11:55:19   │\n│                    │ Ocean migration 2      │       │       │                     │                │ UTC                    │\n└────────────────────┴────────────────────────┴───────┴───────┴─────────────────────┴────────────────┴────────────────────────┘\n\n# Get the audit log for a push\n> pwpush audit <secret url token>\n```\n\n## Show Configuration\n\n```\n> pwpush config show\n\n=== Instance Settings:\nSpecify your credentials and even your private Password Pusher instance here.\n\n┏━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n┃ Key   ┃ Value              ┃ Description                                                            ┃\n┡━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩\n│ URL   │ https://pwpush.com │ The Password Pusher instance to work with.                             │\n│ email │ Not Set            │ E-mail address of your account on Password Pusher.                     │\n│ token │ Not Set            │ API token from your account.  e.g. \'https://pwpush.com/en/users/token\' │\n└───────┴────────────────────┴────────────────────────────────────────────────────────────────────────┘\n\n=== Expiration Settings:\nPushes created with this tool will have these expiration settings.\n\nIf not specified, the application defaults will be used.\nCommand line options override these settings.  See \'pwpush push --help\'\n\n┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n┃ Key                 ┃ Value   ┃ Valid Values ┃ Description                                                      ┃\n┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩\n│ expire_after_days   │ Not Set │ 1-90         │ Number of days each push will be valid for.                      │\n│ expire_after_views  │ Not Set │ 1-100        │ Number of views each push will be valid for.                     │\n│ retrieval_step      │ Not Set │ true/false   │ Require users to perform a click through to retrieve a push.     │\n│ deletable_by_viewer │ Not Set │ true/false   │ Enables/disables a user from deleting a push payload themselves. │\n└─────────────────────┴─────────┴──────────────┴──────────────────────────────────────────────────────────────────┘\n\n=== CLI Settings:\nBehavior settings for this CLI.\n\nCommand line options override these settings.  See \'pwpush --help\'\n\n┏━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n┃ Key     ┃ Value ┃ Valid Values ┃ Description                      ┃\n┡━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩\n│ json    │ False │ true/false   │ CLI outputs results in JSON.     │\n│ verbose │ False │ true/false   │ More verbosity when appropriate. │\n└─────────┴───────┴──────────────┴──────────────────────────────────┘\n\nTo change the above the values see: \'pwpush config set --help\'\n\nUser config is saved in \'/Users/pglombardo/Library/Application Support/pwpush/config.ini\'\n```\n\n# Screenshots\n\n## Help\n\n![](https://disznc.s3.amazonaws.com/pwpush-cli-help.png)\n\n## List\n\n![](https://disznc.s3.amazonaws.com/pwpush-cli-list.png)\n\n## Audit\n\n![](https://disznc.s3.amazonaws.com/pwpush-cli-audit.png)\n\n## Config\n\n![](https://disznc.s3.amazonaws.com/pwpush-cli-config.png)\n',
    'author': 'pwpush',
    'author_email': 'pglombardo@hey.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pglombardo/pwpush',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
