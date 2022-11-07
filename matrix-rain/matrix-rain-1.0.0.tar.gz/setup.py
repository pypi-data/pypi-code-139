# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['matrix_rain']

package_data = \
{'': ['*']}

install_requires = \
['rich>=12.6.0,<13.0.0', 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['matrix_rain = matrix_rain.main:app']}

setup_kwargs = {
    'name': 'matrix-rain',
    'version': '1.0.0',
    'description': '',
    'long_description': '<div align="center">\n    <img src="./demo.gif" width="5000" alt="Demo" />\n    <h1>Matrix Rain</h1>\n    <p>A matrix rain effect written in Python.</p>\n</div>\n\n# Installation\n\n```\npip install matrix-rain\n```\n\n## Usage\n\n```\nmatrix_rain [OPTIONS]\n```\n\nOptions:\n\n-   `--speed`, `-s` - Percentage of normal rain speed. Default: 100\n-   `--glitches`, `-g` - Percentage of normal glitch amount. Default: 100\n-   `--frequency`, `-f` - Percentage of normal drop frequency. Default: 100\n',
    'author': 'principle105',
    'author_email': 'principle105@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
