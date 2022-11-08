from setuptools import setup
setup(
    name='pdflayoutxt',
    version='0.0.5',
    author='Sumeet Suman',
    description='This library helps in extracting text from searchable pdf files.',
    keywords='pdftotext,pdflayout,setuptools',
    python_requires='>=3.6, <4',
    install_requires=['pdfplumber','cleantext','autocorrect'],
    
)