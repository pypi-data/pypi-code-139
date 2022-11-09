from setuptools import setup 
setup(name="iam_userdata",
version="0.3",
description="This a package for creatring a list of iam user from an environmet",
long_description="",
author="Kuldip Sahdeo",
packages=['ct-module'],
install_requires=['boto3','datetime','pandas']
)