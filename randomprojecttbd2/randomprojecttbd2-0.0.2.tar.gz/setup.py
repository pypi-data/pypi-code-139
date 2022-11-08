from setuptools import setup, find_packages
import codecs
import os

# here = os.path.abspath(os.path.dirname(__file__))

# with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
#     long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'Learning to make a py package'
LONG_DESCRIPTION = 'A package that allows to build nothing.'

# Setting up
setup(
    name="randomprojecttbd2",
    version=VERSION,
    author="Noone",
    author_email="<mail@noone.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description = LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy', 'scipy', 'tqdm'],
    keywords=['python', 'terms-related-to-project'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)