from setuptools import setup

setup(
    name='Andrei-first-hello',
    version='0.1.0',
    author='Andrei Panescu',
    author_email='alupanescu@gmail.com',
    packages=['my_own_package'],
    package_dir={'': 'src\\'},
    include_package_data=True
)
