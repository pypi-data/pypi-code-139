from setuptools import setup, find_packages
import os

VERSION = '0.0.48'
DESCRIPTION = 'LIBRA package'
#LONG_DESCRIPTION = 'A package that allows to process and integrate/prediction paired singlecell data.'

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / "README.md").read_text()

# Setting up
setup(
    name="sc_libra",
    version=VERSION,
    author="Xabier Martinez de Morentin",
    author_email="<xabiermm1@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['anndata','numpy','pandas','leidenalg','tensorflow','keras','scanpy','scipy','sklearn','rpy2'],
    keywords=['python', 'singlecell', 'sc', 'integration', 'prediction', 'pipeline'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    # If any package contains *.r files, include them:
    package_data={'': ['*.r', '*.R']},
    include_package_data=True
)

