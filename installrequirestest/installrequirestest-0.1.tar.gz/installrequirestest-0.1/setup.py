from distutils.core import setup
import urllib.request

try:
    import bs4
    print(bs4)
except:
    pass


setup(
  name = 'installrequirestest',
  packages = ['installrequirestest'],
  version = '0.1',
  install_requires=['beautifulsoup4']
)