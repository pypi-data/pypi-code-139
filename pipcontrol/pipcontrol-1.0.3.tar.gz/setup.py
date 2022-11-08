import setuptools

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
import manager

from pipcontrol import pipcontrol

import manager

pipcontrol.install

setuptools.setup(
    name = 'pipcontrol',
    version = '1.0.3',
    description = 'simple python package installer',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author = 'Mingoo Lee',
    author_email = 'labovming@gmail.com',
    keyword = ['python', 'package', 'install', 'update', 'uninstall',
               'pip', 'pip3',],
    python_requires = '>=3.8',
    zip_safe = False,
    license="MIT",
    url = 'https://github.com/labov/python-pip-controller',
    packages = setuptools.find_packages(),
    classifiers = [
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 3 - Alpha',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'Topic :: Software Development :: Libraries :: Python Modules',

    # Pick your license as you wish (should match "license" above)
    'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3.8',

    'Operating System :: OS Independent',
    ],
)