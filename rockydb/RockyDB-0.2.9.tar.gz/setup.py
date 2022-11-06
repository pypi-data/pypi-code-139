# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rockydb']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=5.3.0,<6.0.0',
 'black>=22.10.0,<23.0.0',
 'fastapi>=0.85.1,<0.86.0',
 'flake8>=5.0.4,<6.0.0',
 'furo>=2022.9.29,<2023.0.0',
 'lxml>=4.9.1,<5.0.0',
 'pytest>=7.2.0,<8.0.0',
 'rocksdict==0.2.16',
 'uvicorn>=0.19.0,<0.20.0']

setup_kwargs = {
    'name': 'rockydb',
    'version': '0.2.9',
    'description': 'A NoSQL database.',
    'long_description': '# RockyDB \n[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n![CI](https://github.com/aaldulimi/rockydb/actions/workflows/integrate.yml/badge.svg)\n[![codecov](https://codecov.io/github/aaldulimi/RockyDB/branch/master/graph/badge.svg?token=6MZLCKX5IJ)](https://codecov.io/github/aaldulimi/RockyDB)\n\nSimple document (i.e. NoSQL) database written in Python. It relies on rocksdb as its storage engine. This is more of a Proof-of-concept than a production-ready database. \n\n## Contents\n- [RockyDB](#rockydb)\n  - [Contents](#contents)\n  - [Features](#features)\n  - [Installation](#installation)\n  - [Documentation](#documentation)\n    - [Create collection](#create-collection)\n    - [Insert doucment](#insert-document)\n    - [Get document](#get-document)\n    - [Delete document](#delete-document)\n    - [Query](#query)\n    \n\n\n## Features\nCurrently under active development, however here is the feature list so far:\n\n- **Create collections**\n- **Insert, get and delete documents**\n- **REST API**\n- **Query language**\n- **Full-text Search [IN-DEVELOPMENT]**\n\n## Installation \n```pip install rockydb```\n\n## Documentation\nFull [Documentation](https://rockydb.readthedocs.io/en/latest/). Below are the basics\n### Create collection \n```python\nfrom src.rocky import RockyDB\n\ndb = RockyDB(path="database/")\nnews = db.collection("news")\n```\n\n### Insert document\nSupported data types: `str`, `int`, `float`, `bool` and `list`. Will support more later. \n```python\ndoc_id = news.insert({\n  "title": "Elon Musk Completes $44 Billion Deal to Own Twitter",\n  "year": 2022,\n  "people": ["Elon Musk"],\n  "pi": 3.14,\n  "real": True\n})\n```\nThe `insert` method will return a unique document `_id`.\n\n### Get document\n```python\nnews.get(doc_id)\n```\n### Delete document\n```python\nnews.delete(doc_id)\n```\n### Query\n```python\nnews.find({"pi?lt": 3.14, "real": True}, limit=10)\n``` \nThe `limit` arg is optional. Supports exact, lte, lt, gt and gte queries. Currently working on implementing contains and range queries.\n',
    'author': 'Ahmed',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aaldulimi/RockyDB',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
