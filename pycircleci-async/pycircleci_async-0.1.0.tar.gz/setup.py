# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycircleci_async']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0,<0.24.0', 'python-dateutil>=2.8.2,<3.0.0']

setup_kwargs = {
    'name': 'pycircleci-async',
    'version': '0.1.0',
    'description': 'Async Python client for CircleCI API',
    'long_description': "# pycircleci\n\n[![PyPI version](https://badge.fury.io/py/pycircleci-async.svg)](https://badge.fury.io/py/pycircleci-async)\n[![Build Status](https://github.com/theY4Kman/pycircleci-async/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/theY4Kman/pycircleci-async/actions/workflows/test.yml?query=branch%3Amaster)\n\nAsynchronous Python client for [CircleCI API](https://circleci.com/docs/2.0/api-intro/).\n\nPorted from [pycircleci](https://github.com/alpinweis/pycircleci), a fork of the discontinued [circleci.py](https://github.com/levlaz/circleci.py) project.\n\n## Features\n\n- Supports [API v1.1](https://circleci.com/docs/api/#api-overview) and [API v2](https://circleci.com/docs/api/v2/)\n- Supports both `circleci.com` and self-hosted [Enterprise CircleCI](https://circleci.com/enterprise/)\n\n## Installation\n\n    $ pip install pycircleci-async\n\n## Usage\n\nCreate a personal [API token](https://circleci.com/docs/2.0/managing-api-tokens/#creating-a-personal-api-token).\n\nSet up the expected env vars:\n\n    CIRCLE_TOKEN           # CircleCI API access token\n    CIRCLE_API_URL         # CircleCI API base url. Defaults to https://circleci.com/api\n\n```python\nimport asyncio\nfrom pycircleci_async import CircleCIClient\n\n\nasync def main():\n    async with CircleCIClient(token='<access-token-uuid>') as circle_client:\n        # get current user info\n        await circle_client.get_user_info()\n\n        # get list of projects\n        results = await circle_client.get_projects()\n\n\nasyncio.run(main())\n```\n\n\n### Contributing\n\n1. Fork it\n2. Install poetry (`pip install poetry`)\n3. Install dependencies (`poetry install`)\n4. Create your feature branch (`git checkout -b my-new-feature`)\n5. Make sure `flake8` and the `pytest` test suite successfully run locally\n6. Commit your changes (`git commit -am 'Add some feature'`)\n7. Push to the branch (`git push origin my-new-feature`)\n8. Create new Pull Request\n",
    'author': 'Adrian Kazaku',
    'author_email': 'alpinweis@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
