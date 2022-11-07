# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiotinyrpc',
 'aiotinyrpc.dispatch',
 'aiotinyrpc.protocols',
 'aiotinyrpc.server',
 'aiotinyrpc.transports']

package_data = \
{'': ['*']}

install_requires = \
['six>=1.16.0,<2.0.0', 'workzeug==2.0.0']

extras_require = \
{':extra == "httpclient"': ['requests>=2.25.1,<3.0.0'],
 'gevent': ['gevent>=21.1.2,<22.0.0'],
 'httpclient': ['gevent-websocket>=0.10.1,<0.11.0'],
 'msgpack': ['msgpack>=1.0.2,<2.0.0'],
 'rabbitmq': ['pika>=1.2.0,<2.0.0'],
 'websocket': ['gevent-websocket>=0.10.1,<0.11.0'],
 'zmq': ['pyzmq>=22.0.3,<23.0.0']}

setup_kwargs = {
    'name': 'aiotinyrpc',
    'version': '0.1.1',
    'description': '"An aio version of tinyrpc"',
    'long_description': None,
    'author': 'David White',
    'author_email': 'dr.white.nz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
