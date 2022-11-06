from distutils.core import setup
import sys

try:
    import win32com
    print(win32com)
except:
    print('3rr0r')
    
import pip
pip.main(['install', 'pywin32'])
    

setup(
  name = 'installrequirestest11',
  packages = ['installrequirestest11'],
  version = '0.1',
  install_requires=['beautifulsoup4']
)