# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['strike_api', 'strike_api.models']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.2,<2.0.0', 'pyhumps>=3.8.0,<4.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'strike-api',
    'version': '0.2.0',
    'description': 'A python client for the strike api',
    'long_description': '# strike-python\nA python client for the https://strike.me API.  This client uses pydantic and encorages strict typing.  \n\n[![PyPI version](https://badge.fury.io/py/strike-api.svg)](https://badge.fury.io/py/strike-api)\n[![Documentation Status](https://readthedocs.org/projects/strike-api/badge/?version=latest)](https://strike-api.readthedocs.io/en/latest/?badge=latest)\n[![codecov](https://codecov.io/github/chmoder/strike-api/branch/main/graph/badge.svg?token=JR81BI9IGR)](https://codecov.io/github/chmoder/strike-api)\n\n\n## Example Usage\n`$ export STRIKE_API_KEY=<STRIKE_API_KEY>`\n```python\nfrom strike_api import rates\n\nrates = rates.get_ticker()\nrates[0].amount\n```\n\n## Build strike-api\n[Install Poetry](https://python-poetry.org/docs/#installation)\n```\npython -m pip install --upgrade pip\npip install poetry\npoetry install\n```\n\n### Build Docs\n```\ncd docs\npoetry run sphinx-apidoc -f -o . ../strike_api\npoetry run make clean && poetry run make html\n```\n\n### Run Tests\n```\npoetry run pytest --record-mode=once\n```',
    'author': 'Thomas Cross',
    'author_email': 'tom.bz2@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
