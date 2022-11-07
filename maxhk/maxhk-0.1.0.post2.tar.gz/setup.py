# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['maxhk', 'maxhk.maxhk']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'maxhk',
    'version': '0.1.0.post2',
    'description': 'Set of miscelaneous utils.',
    'long_description': '# Package with miscelaneous utils\n\n## 1 password\n\n```python\ncreds = op.get_item("pypi.org", ["username", "password"])\n# use `creds.username` or `creds.password`\n```\n\n## PyPI\n\nhttps://pypi.org/project/maxhk/\n',
    'author': 'Max',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/maximehk/maxhk_pypi',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
