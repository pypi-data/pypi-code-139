# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['celery_flask_login']

package_data = \
{'': ['*']}

install_requires = \
['Flask-Login>=0.6.2,<0.7.0',
 'Flask>=2.2.2,<3.0.0',
 'celery>=5.2.7,<6.0.0',
 'pytest>=7.2.0,<8.0.0']

setup_kwargs = {
    'name': 'celery-flask-login',
    'version': '0.1.1',
    'description': '',
    'long_description': 'None',
    'author': 'David Sternlicht',
    'author_email': 'd1618033@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
