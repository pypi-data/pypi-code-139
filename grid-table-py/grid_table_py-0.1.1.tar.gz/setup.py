# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grid_table_py', 'grid_table_py.support']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.1,<2.0.0', 'tabulate>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['grid_table_py = grid_table_py.grid_table_py:run']}

setup_kwargs = {
    'name': 'grid-table-py',
    'version': '0.1.1',
    'description': '',
    'long_description': "# grid-table-py\n\n```shell\ngrid_table_py input.md output.md\n```\n\n**Arguments**(Positional):\n1. Path to input Markdown file\n2. Path to file to place output Markdown\n\nThis is a library and command-line tool for converting Markdown files with pipe tables to Markdown files with grid \ntables. Both the pipe tables and the grid tables must be compatible with \n[Pandoc's Markdown](https://pandoc.org/MANUAL.html#pandocs-markdown). \n(This notably supports tables formatted for github-flavored markdown.)\n\nReleased under MIT License. Author @FSharp4\n",
    'author': 'FSharp4',
    'author_email': '33583307+FSharp4@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<3.12',
}


setup(**setup_kwargs)
