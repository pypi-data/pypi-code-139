# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinx_emf', 'sphinx_emf.config', 'sphinx_emf.ecore', 'sphinx_emf.user_hooks']

package_data = \
{'': ['*'], 'sphinx_emf': ['base_templates/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'Sphinx>=4.0',
 'click>=8.1.3,<9.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'pyecore>=0.13,<0.14',
 'sphinx-needs>=1.0.2,<2.0.0',
 'sphinxcontrib-plantuml>=0.24,<0.25',
 'typing-extensions>=4.4.0,<5.0.0']

entry_points = \
{'console_scripts': ['sphinx-emf-cli = sphinx_emf.cli:run']}

setup_kwargs = {
    'name': 'sphinx-emf',
    'version': '0.2.0',
    'description': 'Connect Sphinx-Needs to EMF models.',
    'long_description': '**Complete documentation**: https://sphinx-emf.useblocks.com/\n\nIntroduction\n============\n\nSphinx-EMF makes it possible to exchange data between\n`Eclipse EMF <https://www.eclipse.org/modeling/emf/>`_ ECore models and\n`Sphinx-Needs <https://github.com/useblocks/sphinx-needs>`_.\n\nThis Sphinx extensions comes with 2 main features:\n\n* a CLI script ``sphinx-emf-cli`` that reads an XMI model and writes RST files contain needs objects\n* a Sphinx builder that reads a Sphinx project containing Sphinx-Needs objects and writes an XMI model from it \n\nBoth features require an EMF ECore metamodel.\n',
    'author': 'team useblocks',
    'author_email': 'info@useblocks.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'http://github.com/useblocks/sphinx-emf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<3.11',
}


setup(**setup_kwargs)
