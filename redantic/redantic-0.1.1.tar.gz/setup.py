# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redantic']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.2,<2.0.0', 'redis>=4.3.4,<5.0.0']

setup_kwargs = {
    'name': 'redantic',
    'version': '0.1.1',
    'description': 'Simple redis storage for pydantic objects with an interface of the MutableMapping.',
    'long_description': "# redantic\n[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)\n\nSimple redis storage for pydantic objects with an interface of the MutableMapping.\n\n## Examples\n\n```python\nfrom redantic import RedisDict\nfrom pydantic import BaseModel\nfrom redis import Redis\n\nclass Car(BaseModel):\n    price: float\n    model: str\n\nCarId = int\n\nclient = Redis()\nd = RedisDict[CarId, Car](client=client, name='car_collection', key_type=CarId, value_type=Car)\nd[1] = Car(price=100.5, model='a')\nd[2] = Car(price=200, model='b')\n\nprint(len(d))\nfor i in d:\n    print(d[i])\n```\n\nYou can also use pydantic object as a key.\n\n```python\nclass CarId(BaseModel):\n    id: int\n    type: str\n\nd[CarId(id=1, type='some_type')] = Car(price=100.5, model='a')\n```",
    'author': 'apollon',
    'author_email': 'Apollon76@yandex.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
