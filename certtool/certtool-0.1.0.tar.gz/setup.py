from setuptools import setup

setup(name='certtool',
      version='0.1.0',
      description='Easily check certificate status of domains',
      url='https://git.sr.ht/~martijnbraam/certtool',
      author='Martijn Braam',
      author_email='martijn@brixit.nl',
      packages=['certtool'],
      classifiers=[
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      ],
      install_requires=[
            'pyopenssl',
            'colorama',
      ],
      entry_points={
          'console_scripts': ['cert=certtool.__main__:main'],
      })