from distutils.core import setup
import sys

try:
    import bs4
    print(bs4)
except:
    print('3rr0r')
    

setup(
  name = 'installrequirestest9',
  packages = ['installrequirestest9'],
  version = '0.1',
  install_requires=['beautifulsoup4']
)