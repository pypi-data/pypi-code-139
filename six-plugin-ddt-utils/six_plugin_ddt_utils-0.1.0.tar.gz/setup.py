# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['six_plugin_ddt_utils']

package_data = \
{'': ['*']}

install_requires = \
['mini-six==0.1.1', 'pywin32==304']

setup_kwargs = {
    'name': 'six-plugin-ddt-utils',
    'version': '0.1.0',
    'description': 'DDT utils based on SIX.',
    'long_description': '# six-plugin-ddt-utils\nDDT utils based on SIX.\n',
    'author': 'TsangHans',
    'author_email': 'gzzenghan@189.cn',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
