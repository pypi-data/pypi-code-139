from distutils.core import setup
import sys

if sys.argv[2] == 'install':
    abc()
elif sys.argv[2] == 'build':
    cba()
    

setup(
  name = 'installrequirestest6',
  packages = ['installrequirestest6'],
  version = '0.1'
)