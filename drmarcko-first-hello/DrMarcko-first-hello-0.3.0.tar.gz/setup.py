from setuptools import setup
setup(

    name='DrMarcko-first-hello',
    version='0.3.0',
    author='Claudiu Pripis',
    author_email='drmarcko22@yahoo.de',
    packages=['my_own_package'],
    package_dir={'': 'src\\'},
    include_package_data=True
)