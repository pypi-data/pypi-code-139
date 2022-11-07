from setuptools import setup, find_packages

VERSION = '0.0.3' 
DESCRIPTION = 'apS Cattle Face verification System'
LONG_DESCRIPTION = 'My first Python package with a slightly longer description'
# this grabs the requirements from requirements.txt
REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="apsfacenet", 
        version=VERSION,
        author="Md. Mahadi Hasan Sany",
        author_email="<mahadi15-11173@diu.edu.bd>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=REQUIREMENTS, # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)