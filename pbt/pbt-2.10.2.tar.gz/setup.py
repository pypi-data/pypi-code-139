# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pbt',
 'pbt.console',
 'pbt.package',
 'pbt.package.manager',
 'pbt.package.registry',
 'pbt.vcs']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'hugedict>=2.7.1,<3.0.0',
 'loguru>=0.6.0,<0.7.0',
 'maturin>=0.13.6,<0.14.0',
 'networkx>=2.8.2,<3.0.0',
 'orjson>=3.8.0,<4.0.0',
 'poetry>=1.2.2,<2.0.0',
 'requests>=2.28.0,<3.0.0',
 'semver>=2.13.0,<3.0.0',
 'tomlkit>=0.11.5,<0.12.0',
 'typing-extensions>=4.4.0,<5.0.0']

entry_points = \
{'console_scripts': ['pbt = pbt.__main__:cli']}

setup_kwargs = {
    'name': 'pbt',
    'version': '2.10.2',
    'description': 'A build tool for multiple Python projects in a single repository',
    'long_description': '<h1 align="center">PBT</h1>\n\n<div align="center">\n<b>pbt</b> — A build tool for multiple Python projects in a single repository\n    \n![PyPI](https://img.shields.io/pypi/v/pbt)\n![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)\n[![GitHub Issues](https://img.shields.io/github/issues/binh-vu/pbt.svg)](https://github.com/binh-vu/pbt/issues)\n![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)\n[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)\n\n</div>\n\n## Introduction\n\nHaving all packages in the same repository make it much easier to develop, share, reuse, and refactor code. Building and publishing the packages should not be done manually because it is time-consuming and may be frustrated if the projects are depending on each other. [pbt](https://github.com/binh-vu/pbt) is a tool designed to help make the process easier and faster. It supports building, installing, and updating versions of your packages and their dependencies consistently. It also provides utility commands to help you work with your packages in multi-repositories as if you are working with a monorepo.\n\n## Installation\n\n```bash\npip install -U pbt\n```\n\n## Usage\n\nNote: currently, [pbt](https://github.com/binh-vu/pbt) supports Python packages configured with Poetry (an awesome dependency management that you should consider using).\n\nAssuming that you organized your packages to different sub-folders, each has their own project configuration file (e.g., `pyproject.toml`). You can run the following commands in the root directory (containing your projects). Note: [pbt](https://github.com/binh-vu/pbt) will discover the project based on the project name in its configuration file not the folder name.\n\nYou can also discover the list of commands by running `pbt --help`. Many commands have an option `--cwd` to override the current working directory.\n\n1. **List all packages in the current project, and their dependencies if required**\n\n```bash\npbt list [-d]\n```\n\n- `-d`, `--dev`: Whether to print to the local (inter-) dependencies\n\n2. **Create virtual environment of a package and install its dependencies**\n\n```bash\npbt install [-d] [-v] [-p <package>]\n```\n\n- `-d`: also install dev-dependencies of the package\n- `-v`: verbose\n- `-p`: specify the package we want to build, if empty build all packages.\n\nIf you have encounter some errors during the installation, you can checkout the `pyproject.failed.toml` file that is generated by pbt in `./cache/<package>` folder (relative to your current working directory). For example, on M1 chip, if your python version is `^3.8`, you can\'t use the newer scipy (e.g., >1.8 as it requires python `<3.11`), poetry lock chooses to use an old version `1.6.0`, which typically can\'t build on M1 due to no pre-built numpy for it.\n\n3. **Update all package inter-dependencies**\n\n```bash\npbt update\n```\n\n4. **Clean packages\' build & lock files**\n\n```bash\npbt clean [-p <package>]\n```\n\n- `-p`: specify the package we want to build, if empty build all packages.\n\n6. **Git clone a multi-repository project**\n\n```bash\npbt git clone --repo <repo_url>\n```\n\nClone a repository and check out all of its submodules to their correct branches that we were using last time.\n\n7. **Git update a multi-repository project**\n\n```bash\npbt git update\n```\n\nPull latest changes from the repository, and check out all of its submodules to their correct branches.\n',
    'author': 'Binh Vu',
    'author_email': 'binh@toan2.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/binh-vu/pbt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
