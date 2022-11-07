from distutils.core import  setup
import setuptools
packages = ['Kimbell_test']# 唯一的包名，自己取名
setup(name='Kimbell_test',
	version='1.0',
	author='Kimbell_D',
    packages=packages, 
    package_dir={'requests': 'requests'},)
