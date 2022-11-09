# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fastapi_sa']

package_data = \
{'': ['*']}

install_requires = \
['sqlalchemy[asyncio]>=1.4.43,<2.0.0', 'starlette>=0.20.4']

setup_kwargs = {
    'name': 'fastapi-sa',
    'version': '0.0.1.dev0',
    'description': 'fastapi-sa provides a simple integration between FastAPI and SQLAlchemy in your application',
    'long_description': '# fastapi-sa\n\n![GitHub](https://img.shields.io/github/license/whg517/aio-pydispatch?style=flat-square)\n![PyPI](https://img.shields.io/pypi/v/0.0.1?color=blue&label=pypi&logo=fastapi_sa)\n\nfastapi-sa provides a simple integration between FastAPI and SQLAlchemy in your application.\nyou can use decorators or middleware to transaction management.\n\n## Installing\n\ninstall and update using pip:\n\n```shell\n$ pip install fastapi-sa\n```\n\n## Examples\n\n### Create models for examples, `models.py`\n\n```python\nfrom sqlalchemy import Column, Integer, String\nfrom sqlalchemy.orm import declarative_base\n\nBase = declarative_base()\n\n\nclass Item(Base):\n    """ItemModel"""\n    __tablename__ = \'item\'\n    id = Column(Integer, primary_key=True)\n    name = Column(String(255))\n\n```\n\n### Usage fastapi middleware\n\n```python\nfrom fastapi import FastAPI\nfrom fastapi_sa.database import db\nfrom fastapi_sa.middleware import DBSessionMiddleware\n\nfrom models import Item\n\napp = FastAPI()\ndb.init(url="sqlite+aiosqlite://")\napp.add_middleware(DBSessionMiddleware)\n\n\n@app.put("/items")\nasync def get_users(name: str):\n    async with db() as session:\n        item = Item(name=name)\n        session.add(item)\n    return {\'msg\': \'ok\'}\n```\n\n### Usage other asynchronous database operations\n\n```python\nimport asyncio\nfrom fastapi_sa.database import db, session_ctx\n\nfrom models import Item\n\ndb.init(url="sqlite+aiosqlite://")\n\n\n@session_ctx\nasync def add_data(name: str):\n    async with db() as session:\n        item = Item(name=name)\n        session.add(item)\n\n\nasyncio.run(add_data(\'item_test\'))\n```\n\n## Similar design\n\n- [FastAPI-SQLAlchemy](https://github.com/mfreeborn/fastapi-sqlalchemy)\n\n## Based on\n\n- [FastAPI](https://github.com/tiangolo/fastapi)\n- [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy)\n\n## Develop\n\nYou may need to read the [develop document](./docs/development.md) to use SRC Layout in your IDE.\n\n',
    'author': 'huagang',
    'author_email': 'huagang517@126.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
