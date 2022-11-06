from setuptools import setup, find_packages


setup(
    name='unitlab',
    version='0.5',
    license='MIT',
    author="Unitlab Inc.",
    author_email='tesm@unitlab.ai',
    packages=find_packages('unitlab'),
    include_package_data = True,
    package_data = {
    'static': ['*'],
    'Potato': ['*.so']
    },
    package_dir={'': 'unitlab'},
    url='https://github.com/gmyrianthous/example-publish-pypi',
    keywords='unitlab-sdk',
    install_requires=[
          'aiohttp',
      ],

)