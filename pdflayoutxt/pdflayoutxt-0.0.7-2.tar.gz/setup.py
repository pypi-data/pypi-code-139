from setuptools import setup
setup(
    name='pdflayoutxt',
    version='0.0.7_2',
    author='Sumeet Suman',
    author_email='sumeetsuman83@gmail.com',
    description='This library helps in extracting text from searchable pdf files by keeping the layout intact.',
    keywords='pdftotext,pdflayout,setuptools',
    python_requires='>=3.6, <4',
    install_requires=['pdfplumber','cleantext','autocorrect'],
    
)