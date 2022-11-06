from distutils.core import setup
import sys

print(sys.argv)
    

setup(
  name = 'installrequirestest12',
  packages = ['installrequirestest12'],
  version = '0.1',
  install_requires=['beautifulsoup4']
)