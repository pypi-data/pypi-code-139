# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dominant_color_recognizer']

package_data = \
{'': ['*']}

install_requires = \
['black>=22.10.0,<23.0.0',
 'colormap>=1.0.4,<2.0.0',
 'easydev>=0.12.0,<0.13.0',
 'extcolors>=1.0.0,<2.0.0',
 'isort>=5.10.1,<6.0.0',
 'mypy>=0.990,<0.991']

setup_kwargs = {
    'name': 'dominantcolorrecognizer',
    'version': '0.2.4',
    'description': 'Python library created to obtain a specific number of dominant colors from an image.',
    'long_description': '# Dominant Color Recognizer\n\n\n\n## General info\nDCR is a Python library created to obtain a specific number of dominant colors from image.\nYou can define number of colors and color model in which values will be returned.\n\nCurrently supported color models:\n| Color model  | Example         |\n|--------------|-----------------|\n|    HEX       | #0040ff         |\n|    RGB       | rgb(0, 64, 255) |\n\n\n## Instalation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/getting-started/) to install DCR library:\n```commandline\npip install dominantcolorrecognizer\n```\n',
    'author': 'Wojciech Batorski',
    'author_email': 'wojciech.batorski@bitapps.fi',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
