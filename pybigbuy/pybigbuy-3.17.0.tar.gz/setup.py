# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bigbuy']

package_data = \
{'': ['*']}

install_requires = \
['api-session>=1.3.2,<2.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'pybigbuy',
    'version': '3.17.0',
    'description': 'BigBuy API client in Python',
    'long_description': '# PyBigBuy\n\n**PyBigBuy** is a Python client for BigBuy’s REST API.\n\nNote: PyBigBuy is not affiliated to nor endorsed by BigBuy.\n\n## Coverage\n\nAs of 3.17.0 PyBigBuy implements all API endpoints.\n\n## Install\n\n### Pip\n\n    python -m pip install pybigbuy\n\n### Poetry\n\n    poetry add pybigbuy\n\n## Usage\n\n```python3\nfrom bigbuy import BigBuy\n\n\nclient = BigBuy("your-API-token", "production")\n```\n\n## License\n\nCopyright 2020-2022 [Bixoto](https://bixoto.com/).\n',
    'author': 'Bixoto',
    'author_email': 'info@bixoto.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
