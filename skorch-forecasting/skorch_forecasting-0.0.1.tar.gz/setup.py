from setuptools import setup, find_packages

name = 'skorch_forecasting'
version = '0.0.0'
author = 'ray ray'
description = 'Sklearn interface to state-of-the-art forecasting with ' \
              'neural networks.'

setup(
    name=name,
    version=version,
    author=author,
    packages=find_packages(),
    description=description,
    python_requires='<3.10',
    install_requires=[
        'numpy>=1.22.0',
        'pandas>=1.4.0',
        'scikit-learn>=1.0.0',
        'skorch>=0.10.0',
        'torch>=1.5.0',
        'pytorch-forecasting>=0.9.0'
    ]
)
