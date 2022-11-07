
# from distutils.core import setup

def readme_file():
      with open("README.rst", encoding="utf-8") as rf:
            return rf.read()

from setuptools import setup
setup(name="xiangmutest", version="1.0.0", description="this is a niubi lib",
      packages=["baotest"], py_modules=["baopingjimokuai"], author="ksy",
      author_email="22222@qq.com", long_description=readme_file(),
      url="http://gethub.com.......", license="MIT")