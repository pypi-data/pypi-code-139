from setuptools import setup, find_packages

setup(
    name='awslambdabootstrap',
    description='A library simplifying the boiler plate for python aws lambda functions',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    version="0.0.5",
    license='GPLv3+',
    author="James Davies",
    author_email='james.davies@made.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/malachantrio/aws-lambda-bootstrap',
    keywords='example project',
    install_requires=[
        'structlog',
        'python-json-logger'
    ]
)
