from setuptools import setup, find_packages

setup(
   name='gruzau',
   version='1.0.1',
   author='sherekhan',
   url='https://notabug.org/montarakuono/gruzau',
   packages=find_packages(),
   license='GNU GPL3+',
   description='Extra scripts using uzoenr',
   long_description=open('README.md').read(),
   install_requires=[
       "uzoenr>=25"
   ],
   entry_points={
        'console_scripts':
            ['gruzau-dump = gruzau.dump:start',
            'gruzau-load = gruzau.load:start',
            'gruzau-speak = gruzau.speak:start']
        }
)
