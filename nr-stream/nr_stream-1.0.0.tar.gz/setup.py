# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['stream']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nr-stream',
    'version': '1.0.0',
    'description': '',
    'long_description': '# nr.stream\n\nProvides a useful `Stream` and `Optional` class.\n\n```py\nfrom nr.stream import Stream\n\nvalues = [3, 6, 4, 7, 1, 2, 5]\nassert list(Stream(values).chunks(values, 3, fill=0).map(sum)) == [13, 10, 5]\n```\n',
    'author': 'Niklas Rosenstein',
    'author_email': 'rosensteinniklas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
