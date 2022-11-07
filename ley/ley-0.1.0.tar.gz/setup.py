# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ley']

package_data = \
{'': ['*']}

install_requires = \
['jsonschema>=4.17.0,<5.0.0', 'websockets>=10.4,<11.0']

setup_kwargs = {
    'name': 'ley',
    'version': '0.1.0',
    'description': 'A package for communicating with the Citadel backend.',
    'long_description': '# citadel\n\nA package for communicating with the Citadel backend.\n\n## Installation\n\n```bash\n$ pip install citadel\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`citadel` was created by Miles van der Lely. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`citadel` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Miles van der Lely',
    'author_email': 'milesvanderlely@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
