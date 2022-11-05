from setuptools import setup, find_packages

setup(
    author='Levent Soykan',
    description='Package of helper tools for data science and python',
    name='leventools',
    version='0.1.2',
    packages=find_packages(include=['leventools', 'leventools.*']),
    python_requires='>=3.6',
    install_requires=[
        'numpy>=1.23',
        'pandas>=1.5',
        'scikit-learn>=1.1',
        'scipy>=1.9'
    ]
)
