# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['diffsync', 'diffsync.store']

package_data = \
{'': ['*']}

install_requires = \
['packaging>=21.3,<22.0',
 'pydantic>=1.7.4,<2.0.0,!=1.8,!=1.8.1',
 'structlog>=20.1.0,<22.0.0']

extras_require = \
{'redis': ['redis>=4.3,<5.0']}

setup_kwargs = {
    'name': 'diffsync',
    'version': '1.7.0',
    'description': 'Library to easily sync/diff/update 2 different data sources',
    'long_description': '# DiffSync\n\nDiffSync is a utility library that can be used to compare and synchronize different datasets.\n\nFor example, it can be used to compare a list of devices from 2 inventory systems and, if required, synchronize them in either direction.\n\n# Primary Use Cases\n\nDiffSync is at its most useful when you have multiple sources or sets of data to compare and/or synchronize, and especially if any of the following are true:\n\n- If you need to repeatedly compare or synchronize the data sets as one or both change over time.\n- If you need to account for not only the creation of new records, but also changes to and deletion of existing records as well.\n- If various types of data in your data set naturally form a tree-like or parent-child relationship with other data.\n- If the different data sets have some attributes in common and other attributes that are exclusive to one or the other.\n\n# Overview of DiffSync\n\nDiffSync acts as an intermediate translation layer between all of the data sets you are diffing and/or syncing. In practical terms, this means that to use DiffSync, you will define a set of data models as well as the “adapters” needed to translate between each base data source and the data model. In Python terms, the adapters will be subclasses of the `DiffSync` class, and each data model class will be a subclass of the `DiffSyncModel` class.\n\n![Diffsync Components](https://raw.githubusercontent.com/networktocode/diffsync/develop/docs/images/diffsync_components.png "Diffsync Components")\n\n\nOnce you have used each adapter to load each data source into a collection of data model records, you can then ask DiffSync to “diff” the two data sets, and it will produce a structured representation of the difference between them. In Python, this is accomplished by calling the `diff_to()` or `diff_from()` method on one adapter and passing the other adapter as a parameter.\n\n![Diffsync Diff Creation](https://raw.githubusercontent.com/networktocode/diffsync/develop/docs/images/diffsync_diff_creation.png "Diffsync Diff Creation")\n\nYou can also ask DiffSync to “sync” one data set onto the other, and it will instruct your adapter as to the steps it needs to take to make sure that its data set accurately reflects the other. In Python, this is accomplished by calling the `sync_to()` or `sync_from()` method on one adapter and passing the other adapter as a parameter.\n\n![Diffsync Sync](https://raw.githubusercontent.com/networktocode/diffsync/develop/docs/images/diffsync_sync.png "Diffsync Sync")\n\n# Simple Example\n\n```python\nA = DiffSyncSystemA()\nB = DiffSyncSystemB()\n\nA.load()\nB.load()\n\n# Show the difference between both systems, that is, what would change if we applied changes from System B to System A\ndiff_a_b = A.diff_from(B)\nprint(diff_a_b.str())\n\n# Update System A to align with the current status of system B\nA.sync_from(B)\n\n# Update System B to align with the current status of system A\nA.sync_to(B)\n```\n\n> You may wish to peruse the `diffsync` [GitHub topic](https://github.com/topics/diffsync) for examples of projects using this library.\n\n# Documentation\n\nThe documentation is available [on Read The Docs](https://diffsync.readthedocs.io/en/latest/index.html).\n\n# Installation\n\n### Option 1: Install from PyPI.\n\n```\n$ pip install diffsync\n```\n\n### Option 2: Install from a GitHub branch, such as main as shown below.\n```\n$ pip install git+https://github.com/networktocode/diffsync.git@main\n```\n\n# Contributing\nPull requests are welcomed and automatically built and tested against multiple versions of Python through GitHub Actions.\n\nThe project is following Network to Code software development guidelines and are leveraging the following:\n\n- Black, Pylint, Bandit, flake8, and pydocstyle, mypy\xa0for Python linting, formatting and type hint checking.\n- pytest, coverage, and unittest for unit tests.\n\n# Questions\nPlease see the [documentation](https://diffsync.readthedocs.io/en/latest/index.html) for detailed documentation on how to use `diffsync`. For any additional questions or comments, feel free to swing by the [Network to Code slack channel](https://networktocode.slack.com/) (channel #networktocode). Sign up [here](http://slack.networktocode.com/)\n',
    'author': 'Network to Code, LLC',
    'author_email': 'info@networktocode.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://diffsync.readthedocs.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
