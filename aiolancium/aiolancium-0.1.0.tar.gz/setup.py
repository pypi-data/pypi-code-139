# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiolancium', 'aiolancium.interfaces', 'aiolancium.resources']

package_data = \
{'': ['*']}

install_requires = \
['jsonref>=1.0.0,<2.0.0', 'simple-rest-client==0.5.4']

extras_require = \
{'doc': ['sphinx-rtd-theme>=1.1.1,<2.0.0',
         'sphinxcontrib-contentui>=0.2.5,<0.3.0',
         'sphinx==4.3.1'],
 'test': ['flake8-bugbear==22.9.23',
          'black<=22.8.0',
          'aioresponses>=0.7.3,<0.8.0',
          'flake8>=5.0.4,<6.0.0']}

setup_kwargs = {
    'name': 'aiolancium',
    'version': '0.1.0',
    'description': 'AsyncIO Client for Lancium',
    'long_description': '[![Build Status](https://github.com/giffels/aiolancium/actions/workflows/unittests.yaml/badge.svg)](https://github.com/giffels/aiolancium/actions/workflows/unittests.yaml)\n[![Verification](https://github.com/giffels/aiolancium/actions/workflows/verification.yaml/badge.svg)](https://github.com/giffels/aiolancium/actions/workflows/verification.yaml)\n[![codecov](https://codecov.io/gh/giffels/aiolancium/branch/main/graph/badge.svg)](https://codecov.io/gh/giffels/aiolancium)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/giffels/aiolancium/blob/master/LICENSE)\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n# aiolancium\n\naiolancium is a simplistic python REST client for the Lancium Compute REST API utilizing asyncio. The client itself has\nbeen developed against the [Lancium Compute REST API documentation](https://lancium.github.io/compute-api-docs/api.html).\n\n## Installation\naiolancium can be installed via [PyPi](https://pypi.org/) using\n\n```bash\npip install aiolancium\n```\n\n## How to use aiolancium\n\n```python\nfrom aiolancium.auth import Authenticator\nfrom aiolancium.client import LanciumClient\n\n# Authenticate yourself against the API and refresh your token if necessary\nauth = Authenticator(api_key="<your_api_key>")\n\n# Initialise the actual client\nclient = LanciumClient(api_url="https://portal.lancium.com/api/v1/", auth=auth)\n\n# List details about the `lancium/ubuntu` container\nawait client.images.list_image("lancium/ubuntu")\n\n# Create your hellow world first job.\njob = {"job": {"name": "GridKa Test Job",\n                   "qos": "high",\n                   "image": "lancium/ubuntu",\n                   "command_line": \'echo "Hello World"\',\n                   "max_run_time": 600}}\n\nawait client.jobs.create_job(**job)\n\n# Show all your jobs and their status in Lancium compute\njobs = await client.jobs.show_jobs()\n\n# Delete all your jobs in Lancium compute\nfor job in jobs["jobs"]:\n    await client.jobs.delete_job(id=job["id"])\n```\n',
    'author': 'Manuel Giffels',
    'author_email': 'giffels@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
