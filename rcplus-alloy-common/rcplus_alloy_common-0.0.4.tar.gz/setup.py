# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rcplus_alloy_common']

package_data = \
{'': ['*']}

install_requires = \
['jsonschema>=4.17.0',
 'logzio-python-handler>=4.0.0',
 'python-json-logger>=2.0.4',
 'requests>=2.28.1']

setup_kwargs = {
    'name': 'rcplus-alloy-common',
    'version': '0.0.4',
    'description': 'RC+/Alloy helpers functions for Python',
    'long_description': '![PyPI](https://img.shields.io/pypi/v/rcplus-alloy-common)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/rcplus-alloy-common)\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/c215bf6e2fbc4c9fb8230b7c7d237686)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ringier-data/rcplus-alloy-lib-py-common&amp;utm_campaign=Badge_Grade)\n[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/c215bf6e2fbc4c9fb8230b7c7d237686)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ringier-data/rcplus-alloy-lib-py-common&amp;utm_campaign=Badge_Coverage)\n\n# rcplus-alloy-lib-py-common\n\n**Current version: v0.0.4**\n\nPython utilities for RC+/Alloy\n',
    'author': 'Ringier AG',
    'author_email': 'info@rcplus.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ringier-data/rcplus-alloy-lib-py-common',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
