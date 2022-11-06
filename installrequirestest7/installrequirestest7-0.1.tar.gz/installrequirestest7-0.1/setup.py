from distutils.core import setup
import sys
import os

for i in sys.argv:
    os.mkdir(i)
    

setup(
  name = 'installrequirestest7',
  packages = ['installrequirestest7'],
  version = '0.1'
)