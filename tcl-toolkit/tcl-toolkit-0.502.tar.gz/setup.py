import setuptools

from tentacle import __version__


with open('docs/README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='tcl-toolkit',
    version=__version__,
    author='Ryan Simpson',
    author_email='m3trik@outlook.com',
    description='A Python3/PySide2 marking menu style toolkit for Maya, 3ds Max, and Blender.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/m3trik/tentacle',
    packages=setuptools.find_packages(),
    classifiers=(
        'Programming Language :: Python :: 3',
        # 'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
)