# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['osint_tools',
 'osint_tools.api',
 'osint_tools.api.email',
 'osint_tools.api.email.gmail',
 'osint_tools.api.four_chan',
 'osint_tools.api.rss',
 'osint_tools.db',
 'osint_tools.db.mongo_db',
 'osint_tools.schemas',
 'osint_tools.schemas.rss']

package_data = \
{'': ['*']}

install_requires = \
['feedparser>=6.0.8,<7.0.0',
 'motor>=3.0.0,<4.0.0',
 'pydantic>=1.10.1,<2.0.0',
 'python-jose>=3.3.0,<4.0.0',
 'requests>=2.11',
 'strawberry-graphql[debug-server,fastapi]>=0.139.0,<0.140.0']

setup_kwargs = {
    'name': 'osint-tools',
    'version': '0.2.0',
    'description': '',
    'long_description': '\nTools for working with data.\n',
    'author': 'Alexander Slessor',
    'author_email': 'alexjslessor@gmail.com.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
