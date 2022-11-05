# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['date']

package_data = \
{'': ['*']}

extras_require = \
{':python_version == "3.6"': ['dataclasses>=0.8,<0.9']}

setup_kwargs = {
    'name': 'nr-date',
    'version': '2.0.0',
    'description': '',
    'long_description': '# nr.date\n',
    'author': 'Niklas Rosenstein',
    'author_email': 'rosensteinniklas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
