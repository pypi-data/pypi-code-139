# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['balconyapp']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'balconyapp',
    'version': '0.1.0',
    'description': 'Balcony App template package. Provides the boilerplate for creating new apps.',
    'long_description': '# balcony-app-template\nA template repository for creating new Balcony Apps.\n',
    'author': 'Oguzhan Yilmaz',
    'author_email': 'oguzhanylmz271@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
