from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "Basic library add_one"
LONG_DESCRIPTION = "basic library for testing pypi"

# Setting up
setup(
    name="example_package_ahmed_heakl",
    version=VERSION,
    author="Ahmed Heakl",
    author_email="ahmed.heakl@ejust.edu.eg",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages("main"),
    install_requires=[],
    keywords=["python", "add_one"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
