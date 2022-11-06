from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: POSIX :: Linux',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3'
]

setup(
    name='miscelltools',
    version='0.0.2',
    description='Toolkit containing different ',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Yasser Alemán-Gómez',
    author_email='yasseraleman@gmail.com',
    license='Apache version 2.0',
    classifiers=classifiers,
    keywords='parcellation',
    packages=find_packages(),
    install_requires=['numpy']
)