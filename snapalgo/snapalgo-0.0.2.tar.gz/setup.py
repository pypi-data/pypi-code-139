from setuptools import setup, find_packages
 
 
setup(
  name='snapalgo',
  version='0.0.2',
  description='Various Coding algorithms',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Anish Adnani',
  author_email='anishadnani00@gmail.com',
  license='MIT', 
  keywords=['python', 'coding', 'template', 'algo', 'algorithms'],
  packages=find_packages(),
  install_requires=[''] ,
  classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)