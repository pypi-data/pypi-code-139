from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="package_dio_test01",
    version="0.0.1",
    author="fabiomirandamonte",
    author_email="fabiomirandamonte@gmail.com",
    description="DIO BootCamp UnimedBH",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fabiomirandamonte/-dio-desafio-image-processing-package.git",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)