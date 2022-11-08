from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="escalonamento",
    version="0.0.1",
    author="João",
    author_email="joaodlrio@outlook.com",
    description="Função para escalonar matrizes",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JheyBi/Escalonamento",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)