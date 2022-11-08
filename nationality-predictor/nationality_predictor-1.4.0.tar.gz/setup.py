from setuptools import find_packages, setup

with open("README.md", "r") as fh:
  long_description = fh.read()

setup(
    name = "nationality_predictor",
    version = "1.4.0",
    author = "Thomas Dewitte",
    author_email = "thomasdewittecontact@gmail.com",
    license = "MIT",
    url = "https://github.com/dewittethomas/nationality-predictor",
    
    description = "An engine that predicts the nationality of a person's name",
    long_description = long_description,
    long_description_content_type = "text/markdown",

    package_dir = {"nationality_predictor": "nationality_predictor"},
    install_requires = [
        "requests>=2.28.1"
    ],

    packages = find_packages(),

    classifiers = [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ]
)