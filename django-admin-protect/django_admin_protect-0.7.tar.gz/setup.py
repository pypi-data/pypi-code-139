import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), "README.rst")) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="django_admin_protect",
    version="0.7",
    packages=find_packages(),
    long_description=README,
    author="Shatalov Vladyslav",
    author_email="quantumastelata@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3.10"
    ],
    include_package_data=True,
    include_dirs=True
)