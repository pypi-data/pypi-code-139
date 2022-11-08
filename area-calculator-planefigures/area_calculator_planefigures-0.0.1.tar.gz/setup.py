from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="area_calculator_planefigures",
    version="0.0.1",
    author="Nathanni",
    author_email="nathannivpadua@gmail.com",
    description="Area Calculator Package for flat figures",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NathanniPadua/dio_desafio_criando_o_meu_primeiro_pacote_Python.git",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)