from setuptools import setup, find_packages


setup(
    name='CookJoke',
    version='0.2',
    license='MIT',
    author="Vasilev Ivan",
    author_email='ivan.vasilev.cn@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/cl1ckname/CookJoke',
    keywords='humor',
)