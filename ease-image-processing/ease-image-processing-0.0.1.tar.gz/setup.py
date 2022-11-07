from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name = "ease-image-processing",
    version = "0.0.1",
    author = "Vítor Pereira",
    author_email = "vitorpereira3115@gmail.com",
    description = "A wrapper of scikit image for ease of use",
    long_description = page_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/VitorBSP/ease-image-processing",
    packages = find_packages(),
    install_requires = requirements,
    python_requires = '>=3.8'
)