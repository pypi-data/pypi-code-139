#pip install setuptools
#pip install wheel
#pip install twine

from setuptools import setup, find_packages

#python setup.py sdist bdist_wheel
#makes dist, build, name.egg-info
#twine upload dist/* --verbose

setup(
    name = 'pycraters',
    version = '0.0.4', #even if you delete the dist folder, you have to change the version number
    packages = find_packages(),
    description='A Python framework designed to automate the most common tasks associated with the extraction and upscaling of statistics of single-impact crater functions to inform coefficients of continuum equations describing surface morphology evolution.',
    author='Scott Norris',
    author_email='<snorris@mail.smu.edu>',
    keywords=['craters', 'education'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    install_requires=['numpy', 'matplotlib', 'scipy', 'pandas', 'lmfit', 'uncertainties']
)
