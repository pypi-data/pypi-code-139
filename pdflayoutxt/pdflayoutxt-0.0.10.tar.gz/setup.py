from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name='pdflayoutxt',
    version='0.0.10',
    author='Sumeet Suman',
    author_email='sumeetsuman83@gmail.com',
    description='This library helps in extracting text from searchable pdf files by keeping the layout intact.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='pdftotext,pdflayout,setuptools',
    python_requires='>=3.6, <4',
    install_requires=['pdfplumber','cleantext','autocorrect'],
    
)