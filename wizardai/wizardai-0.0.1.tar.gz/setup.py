from setuptools import setup, find_packages

# TEST_VERSION = '0.0.09' 
VERSION = '0.0.1'
DESCRIPTION = 'Wizard AI Core Package'

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="wizardai", 
        version=VERSION,
        author="Adam Brownell",
        author_email="adam@thewizard.ai",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        url="https://www.thewizard.ai/",
        packages=find_packages(),
        install_requires=[], 
        
        keywords=['python'],
        classifiers= [
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)