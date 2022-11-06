from setuptools import setup, find_packages


setup(
    name='unitlab',
    version='0.6',
    license='MIT',
    author="Unitlab Inc.",
    author_email='tesm@unitlab.ai',
    packages=find_packages('src'),
    include_package_data = True,
    package_data = {
    'static': ['*'],
    'Potato': ['*.so']
    },
    package_dir={'': 'src'},
    url='https://github.com/gmyrianthous/example-publish-pypi',
    keywords='unitlab-sdk',
    install_requires=[
          'aiohttp',
      ],

)