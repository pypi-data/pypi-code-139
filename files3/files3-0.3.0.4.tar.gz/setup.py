from setuptools import setup, find_packages

pkgs = find_packages()

print("packages: ", pkgs)

setup(
    name="files3",
    version="0.3.0.4",
    author="eaglebaby",
    author_email="2229066748@qq.com",
    description="(pickle+lz4 based) save Python objects in binary to the file system and manage them.",

    #url="http://iswbm.com/", 

    packages=pkgs,
    platforms = "",
    classifiers = [
        'Development Status :: 3 - Alpha',

        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Programming Language :: Python :: 3',
    ],

    install_requires=["lz4"],

    python_requires='>=3'


)