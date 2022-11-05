from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='pranyaoptimalpricingmodel1',
  version='0.0.1',
  description='An optimal pricing model that can be used for any new product launched in the market.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Pranya Chandratre',
  author_email='pranya.chandratre002@nmims.edu.in',
  license='MIT', 
  classifiers=classifiers,
  keywords='optimal pricing model', 
  packages=find_packages(),
  install_requires=['scipy'] 
)
