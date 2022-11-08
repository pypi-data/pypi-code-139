
from distutils.core import setup

setup(
    name =          'aiaa-framework',
    version =       '0.0.2',
    description =   'Framework for Koerber Python AI-AA team to simplify data IO and cloud usage.',
    author =        'Körber Supply Chain Software',
    maintainer=     'Körber Supply Chain Software',
    copyright =     'Copyright 2022, PythonBase, Körber Supply Chain Software',
    license =       'Apache 2.0',

    packages = [
        'aiaa',
        'aiaa.utils',
        'aiaa.sql'
    ]
)