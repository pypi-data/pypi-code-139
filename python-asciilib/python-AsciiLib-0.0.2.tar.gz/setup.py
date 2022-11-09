from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'An ascii art package'
LONG_DESCRIPTION = 'A package that makes it easy to convert images and videos to ascii art'

setup(
    name="python-AsciiLib",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Alexander J.",
    author_email="alexandergrahambell707@gmail.com",
    license='MIT',
    packages=find_packages('C:\\Users\\alexa\\Documents\\VSCode\\AsciiLib Package\\AsciiLib'),
    install_requires=[],
    keywords='ascii',
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ]
)