from io import open
from setuptools import setup

version = '1.1'
long_description = 'Python module by developer saivan'

setup(
      name='stern',
      version=version,
      author='saivan',
      author_email='vasilsalkou@gmail.com',
      description=(
            'Python module by developer saivan'
      ),
      long_description=long_description,
      long_description_content_type='text/markdown',

      url='https://github.com/VasilSalkov/stern',
      download_url='https://github.com/VasilSalkov/stern/archive/refs/heads/main.zip'.format(
            version
      ),

      license='GNU General Public License v3.0',

      packages=['stern'],
      classiFiers=[
            'License :: OSI Approved :: GNU General Public License v3.0',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: Implementation :: PyPy',
      ]
)