from setuptools import find_packages, setup

with open("README.rst", "r") as readme:
    long_description = readme.read()

setup(
    name = 'SpectroMap',
    packages = find_packages(include=['spectromap']),
    version = '1.0.1',
    author = 'Aaron Lopez-Garcia',
    author_email='aaron.lopez@uv.es',
    description = 'SpectroMap is a peak detection algorithm that computes the constellation map for a given signal',
    long_description = long_description,
    license = 'GPL-3.0',
    url='https://github.com/Aaron-AALG/SpectroMap',
    download_url = 'https://github.com/Aaron-AALG/SpectroMap/releases/tag/spectromap_1.0.0',
    install_requires=['numpy >= 1.19',
                      'scipy >= 1.6.3'],
    classifiers=["Programming Language :: Python :: 3.8",
			     "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"],
)
