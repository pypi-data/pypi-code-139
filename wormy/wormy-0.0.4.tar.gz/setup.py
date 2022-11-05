from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'Programming Language :: Python',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='wormy',
    version='0.0.4',
    description='Basic Python module made by a middle schoool student for fun',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Sahil',
    author_email='smartluminous213@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='',
    packages=['wormy'],
    install_requires=['']
)