import setuptools

setuptools.setup(
    name='ubit-autolab-commit-parser',
    version='0.0.2',
    description='Simple String Parsing for CICD Demo',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    python_requires='>=3.6, <4',
)
