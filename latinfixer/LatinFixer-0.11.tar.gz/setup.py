from setuptools import setup, find_packages
import codecs
import os

#change to dict
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.11'
DESCRIPTION = "Repair badly decoded latin strings \x00 | \226\130\172 | â€œ | \xe2\x84\xa2 | \u2122 | & #032; | & yuml;"

# Setting up
setup(
    name="LatinFixer",
    version=VERSION,
    license='MIT',
    url = 'https://github.com/hansalemaos/LatinFixer',
    author="Johannes Fischer",
    author_email="<aulasparticularesdealemaosp@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    #packages=[],
    keywords=['html escaped', 'utf-16', 'utf-8', 'utf8', 'ANSI', 'ASCII', 'iso 8859-1', 'latin', 'UTF-8 badly decoded', 'decoding error', 'fix decoding', 'repair decoding', 'delete escape chars'],
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.9', 'Topic :: Scientific/Engineering :: Visualization', 'Topic :: Software Development :: Libraries :: Python Modules', 'Topic :: Text Editors :: Text Processing', 'Topic :: Text Processing :: General', 'Topic :: Text Processing :: Indexing', 'Topic :: Text Processing :: Filters', 'Topic :: Utilities'],
    install_requires=[],
    include_package_data=True
)
#python setup.py sdist bdist_wheel
#twine upload dist/*