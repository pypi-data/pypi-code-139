from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]




setup(
    name='dsp_house_prices_muktar',
    version='0.0.2',
    description='A package to help load, preprocess, train, evaluate, and predict house prices based on features given in .csv file',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Abubakar M. Muktar',
    author_email='sadiksmart0@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='',
    packages=find_packages(),
    py_modules=["load","preprocess","train","evaluate","inference"]

)