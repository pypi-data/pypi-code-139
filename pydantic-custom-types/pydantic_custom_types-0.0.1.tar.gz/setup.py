# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_custom_types', 'pydantic_custom_types.kubernetes']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pydantic-custom-types',
    'version': '0.0.1',
    'description': 'Custom types for pydantic used in SRE peipelins for validation input vars',
    'long_description': '# pydantic custom types\ndistributes custom types instead of copy pasting code for pipelines input validation',
    'author': 'per lejon',
    'author_email': 'per.lejon@netigate.se',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
