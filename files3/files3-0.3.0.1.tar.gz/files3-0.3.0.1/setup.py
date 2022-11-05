from setuptools import setup, find_packages

setup(
    name="files3",
    version="0.3.0.1",
    author="eaglebaby",
    author_email="2229066748@qq.com",
    description="(pickle+lz4 based) save Python objects in binary to the file system and manage them.",

    #url="http://iswbm.com/", 

    packages=find_packages(),
    platforms = "",
    classifiers = [
        'Development Status :: 3 - Alpha',

        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Programming Language :: Python :: 3',
    ],

    install_requires=["lz4"],

    python_requires='>=3'


)