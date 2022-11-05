# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytest_richtrace']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.2.0,<8.0.0', 'rich>=12.6.0,<13.0.0']

entry_points = \
{'pytest11': ['pytest-richtrace = pytest_richtrace']}

setup_kwargs = {
    'name': 'pytest-richtrace',
    'version': '0.1.0',
    'description': '',
    'long_description': '# pytest-richtrace\n\nA pytest plugin that dumps the stages of the pytest testing process to the terminal.\n\nIt uses `rich` to add formatting to the output.\n\n## Sample output\n\n### Using --collect-only\n\n```shell\npytest -q --collect-only --rich-trace\n```\n\n<img src="./docs/output-collect-only.svg" style="width: 70rem;"/>\n\n### Full test run\n\n```shell\npytest -q --rich-trace\n```\n\n<img src="./docs/output.svg" style="width: 70rem;"/>\n',
    'author': 'Simon Kennedy',
    'author_email': 'sffjunkie+code@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
