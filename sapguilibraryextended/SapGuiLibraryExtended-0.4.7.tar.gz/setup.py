from setuptools import setup
import pathlib

setup(
    name='SapGuiLibraryExtended',
    version='0.4.7',
    description='SOVOS SAP GUI Library for Robot Framework',
    url='https://SovosGvatLatam@dev.azure.com/SovosGvatLatam/"SAP%20Labs"/_git/SovosSAPLibrary',
    long_description='Library to run Robot Framework on SAP GUI',
    long_description_content_type="text/markdown",
    author='Daniela Silva',
    author_email='daniela.silva@sovos.com',
    license="MIT",
    packages=['SapGuiLibraryExtended'],
    include_package_data=True,

    classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Python',
    ],


    )