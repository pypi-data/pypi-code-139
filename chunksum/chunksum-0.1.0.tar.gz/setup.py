# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chunksum']

package_data = \
{'': ['*']}

install_requires = \
['fastcdc>=1.4.2,<2.0.0', 'tqdm>=4.64.1,<5.0.0']

entry_points = \
{'console_scripts': ['chunksum = chunksum.chunksum:main']}

setup_kwargs = {
    'name': 'chunksum',
    'version': '0.1.0',
    'description': 'Print FastCDC rolling hash chunks and checksums.',
    'long_description': '# chunksum\nPrint FastCDC rolling hash chunks and checksums.\n',
    'author': 'Xie Yanbo',
    'author_email': 'xieyanbo@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/xyb/chunksum',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
