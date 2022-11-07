from setuptools import setup, find_packages
from setuptools.command.install import install
import socket
import getpass
import os

class CustomInstall(install):
    def run(self):
        install.run(self)
        print('run custominstall successfully!')


setup(
        name='hachoir3', #package name
        version='5.0.0',
        description='A sample Python project, do not download it!',
        author='MC checker',
        license='MIT',
        packages=find_packages(),
        cmdclass={'install': CustomInstall},
        author_email='zhuzhuzhuzai@gmail.com',
        install_requires=[
                "Alexsecdemo==1.3.4",
                "Bfixsecdemo==1.0.1",
                "requests"
        ],
)
