# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scramblery']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'scramblery',
    'version': '1.2',
    'description': '',
    'long_description': '# Scramblery\n\n[![Downloads](https://pepy.tech/badge/scramblery)](https://pepy.tech/project/scramblery)\n[![PyPI version](https://badge.fury.io/py/scramblery.svg)](https://badge.fury.io/py/scramblery)\n[![Jekyll site CI](https://github.com/altunenes/scramblery/actions/workflows/jekyll.yml/badge.svg)](https://github.com/altunenes/scramblery/actions/workflows/jekyll.yml)\n\nA simple tool to scramble your images or only faces from images or videos. You can find the online demo in javascript [here](https://altunenes.github.io/scramblery/scramblerydemo.html). For more information, please visit the [documentation](https://altunenes.github.io/scramblery/).\n\n#### Purpose of Package\n\nThe purpose of this package is the creating scrambled images from images or videos. User can either scramble the whole image or only facial area.\nThis is very useful tool in psychology experiments especially if you are working with faces. With a for loop you can scramble all the images in a folder and create a new folder with scrambled images. It was very long process to scramble images manually in the past and I feel like this package can be useful for many people. Hope this package will be useful for your research.\n\n#### **Features**\n\n- Scramble whole image with desired degree of scrambling (pixel values or pixel coordinates)\n- Scramble only facial area with desired degree of scrambling (pixel values or pixel coordinates)\n- Scramble only facial area in a video (useful for dynmaic stimuli) with desired degree of scrambling\n\n#### Installation\n\n- The package can be found in pypi. To install the package, run the following command in the terminal:\n- `pip install scramblery`\n\n#### Author\n\n- Main Maintainer: [Enes ALTUN]\n\n#### Usage\n\nAfter installing the package, you can import the package as follows:\n\n- `from scramblery import scramblery`\n  Then use the functions as follows to scramble images. I added some examples below.\n\n  ![8x8](../docs/assets/usage.PNG)\n\n### Contributon\n\nAny kind of contribution is welcome.\n',
    'author': 'altunenes',
    'author_email': 'enesaltun2@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/altunenes/scramblery',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
