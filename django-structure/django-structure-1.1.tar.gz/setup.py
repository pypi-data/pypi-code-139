# -*- encoding: utf-8 -*-
import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-structure',
    version='1.1',
    packages=find_packages(),
    include_package_data=True,
    data_files=[],
    install_requires=[
        'djangorestframework>=3.12.4',
        'django>=3.0.0',

    ],
    python_requires=">=3.8",
    description='Structure for django.',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/ArefMousakhani/django-structure',
    author='Aref Mousakhani',
    author_email='aref.mousakhani@gmail.com',
)
