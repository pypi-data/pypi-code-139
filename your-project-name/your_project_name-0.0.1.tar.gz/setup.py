# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['your_project_name']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=4,<5']}

setup_kwargs = {
    'name': 'your-project-name',
    'version': '0.0.1',
    'description': 'Short description of your project',
    'long_description': "# Your Project Name\n\n<!-- begin badges -->\n\n[![Status][status badge]][status link]\n[![Python Version][python version badge]][pypi package page]\n[![Package Version][pypi latest version]][pypi package page]\n[![Package Downloads][pypi downloads]][pypi package page]\n\n[![License][license]][license]<br>\n[![pre-commit enabled][pre-commit badge]][pre-commit project]\n[![Black codestyle][black badge]][black project]\n\n[status badge]: https://ci.jamesveitch.xyz/api/badges/james/your-project-name/status.svg\n[status link]: https://ci.jamesveitch.xyz/james/your-project-name\n[python version badge]: https://img.shields.io/pypi/pyversions/your_project_name\n[pypi latest version]: https://img.shields.io/pypi/v/your_project_name\n[pypi package page]: https://pypi.org/project/your_project_name/\n[pypi downloads]: https://img.shields.io/pypi/dm/your_project_name\n[license]: https://img.shields.io/pypi/l/your_project_name\n[pre-commit badge]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n[pre-commit project]: https://pre-commit.com/\n[black badge]: https://img.shields.io/badge/code%20style-black-000000.svg\n[black project]: https://github.com/psf/black\n\n<!-- end badges -->\n\nShort description of your project\n\nThis project was generated with the [python-cookiecutter](https://git.jamesveitch.xyz/james/python-cookiecutter) template and, amongst other things, provides the following functionality out of the box.\n\n- CI/CD integration with Woodpecker-CI pipelines\n- Testing via Nox across multiple python versions\n- PyTest integration with codecoverage, mocking and asyncio\n- Linting with black and flake8\n- Type checking with MyPy\n- Security using bandit and safety\n- Documentation via MkDocs with a material theme and autodoc\n  - Live reload during development with `make docs` Makefile\n  - Deployment to GitHub Pages through woodpecker pipeline using [mike](https://github.com/jimporter/mike) for version control\n- Package versioning and build with Poetry\n  - Deployment to both pypi (production) and test.pypi (development) through woodpecker pipelines based on branch\n\n## 📚 Documenation\n\nDocumentation is hosted with GitHub Pages and can be found at:\n\n- ✅ [your-project-name/stable](https://darth-veitcher.github.io/your-project-name/latest/stable) (reflecting the `Master` branch); or\n- ⚠️ [your-project-name/develop](https://darth-veitcher.github.io/your-project-name/latest/develop) (for bleeding edge).\n\n## \xa0⚒️ Installation\n\n**Python Version:** This library is tested against Python >=3.7\n\nTo install the library run this command in your terminal.\n\n```zsh\npip install your_project_name\n```\n\n## 🚀 Usage\n\nTODO: improve documentation here\n\n```py\n>>> import your_project_name\n>>> your_project_name.__version__\n'0.0.1'\n```\n",
    'author': 'James Veitch',
    'author_email': '1722315+darth-veitcher@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://darth-veitcher.github.io/your-project-name/latest',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
