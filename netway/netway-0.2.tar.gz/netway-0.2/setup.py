from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='netway',
    version='0.2',
    license='MIT',
    author="Thesaderror & Mein",
    author_email='saderroraz@protonmail.com',
    packages=find_packages('src'),
    package_dir={'./netway': 'src'},
    url='',
    keywords='sockets, request, http, https, get, port, fast',
    install_requires=[
          'sockets',
          'threading',
          'urllib3',
      ],

)