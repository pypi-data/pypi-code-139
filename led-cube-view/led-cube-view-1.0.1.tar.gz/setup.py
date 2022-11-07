# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['led_cube_view', 'led_cube_view.tools']

package_data = \
{'': ['*'], 'led_cube_view': ['config/*']}

install_requires = \
['PyOpenGL>=3.1.6,<4.0.0',
 'numpy-stl>=2.17.1,<3.0.0',
 'pyqtgraph>=0.13.1,<0.14.0']

extras_require = \
{':python_version >= "3.10" and python_version < "3.12"': ['PySide6>=6.3.1,<7.0.0']}

setup_kwargs = {
    'name': 'led-cube-view',
    'version': '1.0.1',
    'description': 'A PySide6 widget to display a LED cube on a 3D graph and manipulate its LEDs.',
    'long_description': '# led-cube-view\nA PySide6 widget to display a LED cube on a 3D graph and manipulate its LEDs.\nThis is being developed for use with my [LED cube animation editor](https://github.com/crash8229/led-cube-animation-editor).\n',
    'author': 'crash8229',
    'author_email': 'mu304007@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/crash8229/led-cube-view',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
