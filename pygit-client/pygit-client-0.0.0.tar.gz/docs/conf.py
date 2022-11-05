import sphinx_rtd_theme

from importlib.metadata import version

# Project Information
project = 'pygit-client'
copyright = '2022, Lance Eftink'
author = 'Lance Eftink'

release = version(project)
version = '.'.join(release.split('.')[:2])

# Configuration
extensions = [
    'sphinx_rtd_theme'
]

templates_path = ['_templates']
exclude_patterns = []



# HTML Output Configuration
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
