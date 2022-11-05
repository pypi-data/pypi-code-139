# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aio9p', 'aio9p.dialect', 'aio9p.example']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aio9p',
    'version': '0.2.0',
    'description': '',
    'long_description': '# aio9p\n\nAsyncio-based bindings for the 9P protocol. Work in progress.\n\nWorking examples for the 9P2000 9P2000.u dialects are implemented in aio9p.example .\n\n# TODO\n\n## Features\n- Support for the 9P2000.L dialect\n- Message generation and parsing from the client perspective\n\n## Testing\n- Significantly expanded unit testing\n- Integration tests\n- Benchmarking\n',
    'author': 'florp',
    'author_email': 'jens.krewald@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
