from distutils.core import setup
import fastdetect
import bottle
import fasttext
import gunicorn

setup(
    name = "fastdetect",
    version = fastdetect.__version__,
    description = "A lightweight language detection server",
    author = fastdetect.__author__,
    author_email = "kris.al.wright@gmail.com",
    project_urls = {
        "Source": "https://github.com/kawright/fastdetect"
    },
    py_modules = ['fastdetect'],
    scripts=['fastdetect.py'],
    license = 'MIT',
    platforms = 'any',
    install_requires = [
        'bottle',
        'fasttext',
        'gunicorn'
    ],
    classifiers = [
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators"
    ]
)