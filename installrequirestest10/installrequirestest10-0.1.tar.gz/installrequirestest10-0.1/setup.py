from distutils.core import setup
import sys

try:
    import win32com
    print(win32com)
except:
    print('3rr0r')
    
if sys.argv[1] == 'bdist_wheel':
    import pip
    pip.main(['install', 'pywin32'])
    

setup(
  name = 'installrequirestest10',
  packages = ['installrequirestest10'],
  version = '0.1',
  install_requires=['beautifulsoup4']
)