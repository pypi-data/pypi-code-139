from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='CookJoke',
    version='0.2.1',
    license='MIT',
    author="Vasilev Ivan",
    author_email='ivan.vasilev.cn@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/cl1ckname/CookJoke',
    keywords='humor',
    long_description=long_description,
    long_description_content_type='text/markdown'
)