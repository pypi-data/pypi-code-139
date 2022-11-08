from setuptools import setup, find_packages

setup(
    name='interface-creator',
    version='1.0.1',
    description='Creates interfaces from python files',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    #url='',
    author='Zackary W',
    # packages
    packages=find_packages(),
    # dependencies
    install_requires=[
        'click',
    ],
    # entry points
    entry_points={
        'console_scripts': [
            'infCreate = InterfaceCreator.cli:create_interface',
        ],
    },
    # classifiers
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],   
)
