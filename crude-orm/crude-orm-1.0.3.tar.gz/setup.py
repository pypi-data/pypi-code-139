from distutils.core import setup
import crude

setup(
    name = "crude-orm",
    version = crude.__version__,
    description = "A descriptive ORM for Python",
    author = crude.__author__,
    author_email = "kris.al.wright@gmail.com",
    long_description=crude.__doc__,
    long_description_content_type="text/markdown",
    url="https://crudepy.org",
    project_urls = {
        "Source": "https://github.com/kawright/crude"
    },
    py_modules = ['crude'],
    license = 'MIT',
    platforms = 'any',
    classifiers = [
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Database",
        "Topic :: Software Development"
    ]
)