# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['professional_python_exercises_2_githubcli']

package_data = \
{'': ['*']}

install_requires = \
['pygithub>=1.56,<2.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.6.0,<13.0.0',
 'typer>=0.6.1,<0.7.0']

setup_kwargs = {
    'name': 'professional-python-exercises-2-githubcli',
    'version': '0.1.0a0',
    'description': 'Command Line Interface for GitHub as part of the professional python course',
    'long_description': '# Exercise2: GitHub Command line interface (CLI)\n\n## Purpose\n\nThis is the second exercise for the professional python course. The purpose is to build a proper CLI using the github API.\nThe task is (copied from the professional python course): \n\nCreate a python program to interact with GitHub and retrieve data.\nAdd the following commands:\n\n- Count all stars of all repos of yourself, a specified user or an organization.\n- Print out details about yourself, a user or organization.\n  Allow a nicely printed format as default and offer output as json too.\n- One of the following:\n  - (easy) Modify your user description by adding a tea emoji and a heart.\n  - (difficult) Set your user status (top-right when clicking on username)\n    to a tea emoji with the message "Drinking Tea".\n\nFocus points:\n\n- End-users will use your program so focus on usability\n- Integrate previous lessons as much as it makes sense\n\n## Quickstart\n\n### Installing\n\nThis repository uses poetry to install the dependencies and taskfile to execute the most basic functionality. \nAfter having installed taskfile onto your system you can simply use ```task install``` to install the necessary dependendcies into a virtual environment. 4\nBesides the dependencies you will need a GitHub Access Token to use this program. Get it [here]("https://github.com/settings/tokens).\n\n### Usage\n\nPromt ```task``` to get a list of the tasks availabe and go for one of the options: \n\n```bash\n$ task\ntask: Available tasks for this project:\n* build:                Builds the puthon package\n* docs-publish:         Publish the documentation to gh-pages\n* docs-serve:           Serve the documentation locally\n* getdetails:           Get details of a given user and print it to console\n* getdetailsjson:       Get details of a given user in json\n* install:              Installs the dependecies based on the poetry file\n* lint:                 Runs formatting and linting\n* sbom:                 Generate the Software Bill of Materials\n* stars:                Get the number of stars of the given user\'s repositories\n* starsjson:            Get the number of stars of the given user\'s repositories in json format\n* status:               Set the status of your user to something delicous\n* test:                 Runs tests on the code\n```\n\nThe other way of using this tool is directly with calling etiher poetry or native python to start on of the functions, like \n\n```bash\npoetry run python professional_python_exercises_2_githubcli/github_cli.py setstatus\n```\n',
    'author': 'Manuel Ramsaier',
    'author_email': 'manuel.ramsaier89@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
