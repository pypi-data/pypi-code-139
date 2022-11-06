from distutils.core import setup
import sys

if sys.argv[1] == 'install':
    abc()
elif sys.argv[1] == 'build':
    cba()
    

setup(
  name = 'installrequirestest4',
  packages = ['installrequirestest4'],
  version = '0.1'
)