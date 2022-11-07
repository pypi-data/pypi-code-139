# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dbt',
 'dbt.adapters.fal',
 'dbt.adapters.fal_experimental',
 'dbt.adapters.fal_experimental.support',
 'dbt.adapters.fal_experimental.telemetry',
 'dbt.adapters.fal_experimental.teleport_support',
 'dbt.adapters.fal_experimental.utils',
 'dbt.fal.adapters.python',
 'dbt.fal.adapters.teleport',
 'dbt.include.fal',
 'dbt.include.fal_experimental']

package_data = \
{'': ['*'],
 'dbt.include.fal': ['macros/*', 'macros/materializations/*'],
 'dbt.include.fal_experimental': ['macros/*', 'macros/materializations/*']}

install_requires = \
['backports.functools_lru_cache>=1.6.4,<2.0.0',
 'dbt-core>=1.3.0b1,<1.4',
 'isolate[grpc]>=0.3.0,<0.4.0',
 'pandas>=1.3.4,<2.0.0',
 'posthog>=1.4.5,<2.0.0',
 's3fs>=2022.8.2',
 'sqlalchemy>=1.4.41,<2.0.0']

extras_require = \
{'bigquery': ['google-cloud-bigquery[pandas]>=2,<3'],
 'redshift': ['sqlalchemy-redshift>=0.8.9,<0.9.0'],
 'snowflake': ['snowflake-connector-python[pandas]>=2.7.10,<2.8.0']}

setup_kwargs = {
    'name': 'dbt-fal',
    'version': '1.3.1',
    'description': 'Simplest way to run dbt python models.',
    'long_description': None,
    'author': 'Features & Labels',
    'author_email': 'hello@fal.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.2,<3.11',
}


setup(**setup_kwargs)
