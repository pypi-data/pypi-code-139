# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['metaflow_extensions',
 'metaflow_extensions.outerbounds',
 'metaflow_extensions.outerbounds.config',
 'metaflow_extensions.outerbounds.plugins',
 'metaflow_extensions.outerbounds.plugins.kubernetes',
 'metaflow_extensions.outerbounds.toplevel',
 'metaflow_extensions.outerbounds.toplevel.plugins.kubernetes']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.24.37,<2.0.0',
 'kubernetes>=24.2.0,<25.0.0',
 'metaflow>=2.7.2,<3.0.0']

setup_kwargs = {
    'name': 'outerbounds',
    'version': '0.1.1',
    'description': '',
    'long_description': '',
    'author': 'Oleg Avdeev',
    'author_email': 'oleg@outerbounds.co',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
