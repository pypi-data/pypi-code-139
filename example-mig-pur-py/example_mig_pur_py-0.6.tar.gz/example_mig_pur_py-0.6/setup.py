from setuptools import setup, find_packages


setup(
    name='example_mig_pur_py',
    version='0.6',
    license='MIT',
    author="Giorgos Myrianthous",
    author_email='email@example.com',
    packages=find_packages(),
    package_dir={},
    url='https://github.com/gmyrianthous/example-publish-pypi',
    keywords='example project',
    install_requires=[
          'scikit-learn',
      ],

)
