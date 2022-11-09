# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netcheck']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'dnspython>=2.2.1,<3.0.0', 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['netcheck = netcheck.cli:cli']}

setup_kwargs = {
    'name': 'netcheck',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Network Health Check\n\nConfigurable command line application that can be used to test network conditions are as expected.\n\nVery early work in progress version!\n\npoetry \n\nExample:\n\n```\n$ poetry run netcheck check --type=dns --should-fail\nPassed but was expected to fail.\n{\'type\': \'dns\', \'nameserver\': None, \'host\': \'github.com\', \'A\': [\'20.248.137.48\']}\n```\n\n### Individual Assertions\n\n```\n./netcheck check --type=dns --server=1.1.1.1 --host=hardbyte.nz --should-fail\n./netcheck check --type=dns --server=1.1.1.1 --host=hardbyte.nz --should-pass\n./netcheck check --type=http --method=get --url=https://s3.ap-southeast-2.amazonaws.com --should-pass\n```\n\nOutput is quiet by default, json available with `--json` (TODO).\n\npython -m netcheck.cli --help\n\n## Configuration via file\n\nA json file can be provided with a list of assertions to be checked:\n\n```json\n{\n  "assertions": [\n    {"name":  "deny-cloudflare-dns", "rules": [{"type": "dns", "server":  "1.1.1.1", "host": "github.com", "expected": "pass"}] }\n  ]\n}\n```\n\nAnd the command can be called:\n\n$ poetry run netcheck run --config config.json \n\n',
    'author': 'Brian Thorne',
    'author_email': 'brian@thorne.link',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
