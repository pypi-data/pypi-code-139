
from distutils.core import  setup
import setuptools
packages = ['zgx']# 唯一的包名，自己取名
setup(name='zgx',
  version='1.0',
  author='zhang',
    packages=packages, 
    package_dir={'requests': 'requests'},)
