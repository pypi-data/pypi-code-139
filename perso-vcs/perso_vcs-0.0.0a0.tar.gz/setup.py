# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['perso', 'perso.vcs', 'perso.vcs.hashing']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'pydantic>=1.10.2,<2.0.0']

extras_require = \
{':python_version < "3.11"': ['tomli>=2.0.1,<3.0.0']}

setup_kwargs = {
    'name': 'perso-vcs',
    'version': '0.0.0a0',
    'description': 'Version control system for Perso.',
    'long_description': '# Perso.VCS Module\n\n[![pipeline status](https://git.estsoft.com/hunet-ai/Perso.VCS/badges/master/pipeline.svg)](https://git.estsoft.com/hunet-ai/Perso.VCS/commits/master)\n[![coverage report](https://git.estsoft.com/hunet-ai/Perso.VCS/badges/master/coverage.svg)](https://git.estsoft.com/hunet-ai/Perso.VCS/commits/master)\n\nPerso.VCS Module (`perso.vcs`) is a python module for version control of Perso.\n\n## Install\n\n### From PyPI\n\n`pip insall perso.vcs`\n\n### From source\n\nUse of virtual environment is strongly encouraged.\n\n```bash\ngit clone https://github.com/moonsikpark/perso.vcs\ncd perso.vcs\npython -m pip install -U pip setuptools poetry\npoetry install\n```\n',
    'author': 'Moonsik Park',
    'author_email': 'moonsik.park@estsoft.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<=3.11',
}


setup(**setup_kwargs)
