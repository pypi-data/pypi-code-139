# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['morpion-game']

package_data = \
{'': ['*'],
 'morpion-game': ['dist/__main__/*',
                  'dist/__main__/certifi/*',
                  'dist/__main__/lib-dynload/*']}

install_requires = \
['art>=5.2,<6.0', 'requests>=2.26.0,<3.0.0', 'termcolor>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'morpion-game',
    'version': '0.6.1',
    'description': 'A minimal Morpion game to play in the console or with a graphical user interface',
    'long_description': "# Morpion\n\n## installation\nYou can install the package by running the following command : ```python3 -m pip install --upgrade morpion-game``` \n\n### Setup\nThe first time you play, you will be prompted for your favorite language.\nCurrently, the available languages are :\n- English\n- French\n\nOnce done, you can start playing !\n\n### install the GUI\nThe CUI application can be installed directly from the package. You just have to run it with the `--gui` argument.\nThis will launch the GUI application if installed (and found on your system), else it will run the installer program.\n\n#### Notes\nThe CLI and teh GUI applications' datas are shared.\nThese datas are **only** stored on your local machine and will never be publish or send because of the game.\nYou can access datas in your personal directory `C:\\Users\\username\\PetchouDev\\datas.json`. *but do not edit them... I should encrypt them in a next version...*\nYou can delete datas from any of the two applications from the **settings** menu.",
    'author': 'PetchouDev',
    'author_email': 'petchou91d@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/P-C-Corp/Games/Morpion',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
