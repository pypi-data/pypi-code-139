from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="calc_gabrielrs",
    version="0.0.1",
    author="Gabriel R.S.",
    author_email="gabriel.shiota@gmail.com",
    description="",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gabrielrsh/criacao-pacotes-python",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.0',
)