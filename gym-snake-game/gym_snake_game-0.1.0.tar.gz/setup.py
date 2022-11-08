# https://github.com/NaLooo/Gym_Snake_Game

from setuptools import setup, find_packages
import io
from os import path

# --- get version ---
version = "unknown"
with open("gym_snake_game/version.py") as f:
    line = f.read().strip()
    version = line.replace("VERSION = ", "").replace("'", '')
# --- /get version ---

here = path.abspath(path.dirname(__file__))
with io.open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='gym_snake_game',
    version=version,
    description='Snake game for OpenAI Gym',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/NaLooo/Gym_Snake_Game',
    author='Ming Yu',
    author_email='ming.yu@alumni.stonybrook.edu',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',

        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Games/Entertainment :: Arcade',

        'Programming Language :: Python :: 3.10',
    ],
    platforms=['any'],
    keywords='ai, rl, snake',
    packages=find_packages(),
    python_requires='>=3.0',
    install_requires=['pygame>=2.1.0', 'numpy>=1.15', 'gym>=0.26.2'],
)
