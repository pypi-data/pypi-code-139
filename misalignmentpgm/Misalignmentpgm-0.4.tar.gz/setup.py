from setuptools import setup, find_packages

VERSION = '0.4' 
DESCRIPTION = 'My first Python package'
LONG_DESCRIPTION = 'My first Python package with a slightly longer description'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="Misalignmentpgm", 
        version=VERSION,
        author="Supriya",
        author_email="<supriyasuhas058@email.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=['Misalignmentpgm'],

       install_requires=['pandas','matplotlib','paho-mqtt','numpy','scipy','scikit-learn','matplotlib','logging','Werkzeug','flask','Flask-API','concurrent_log_handler','requests','waitress','nltk'],
       


        # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        )