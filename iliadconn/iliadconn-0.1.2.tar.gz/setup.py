from setuptools import setup, find_packages

version = {}
exec(open('iliad/_version.py').read(), version)
setup(
    name='iliadconn',
    version=version['__version__'],
    packages=find_packages(),
    url='',
    license='GPL',
    author='massimo',
    author_email='massimo.cavalleri@gmail.com',
    description='get monthly outgoing traffic per iliad SIM',
    install_requires=[
        'beautifulsoup4',
        'lxml',
        'requests',
        'python-dateutil',
        'appdirs'
    ],
    entry_points={
        'console_scripts': [
            'iliadconn=iliad.iliadconn:main',
        ],
    }
)
