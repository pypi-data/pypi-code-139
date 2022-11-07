from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="gerador_senhas",
    version="0.0.2",
    author="Rafael Rodrigues Mateus",
    author_email="rafael.r.mateus@gmail.com",
    description="Pacote para gerar senhas aleatórias contendo números, letras e caracteres especiais.",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Raf-RM/Bootcamp-Geracao-Tech-Unimed-BH-Ciencia-de-Dados/tree/master/Python-para-cientistas-de-dados/Projeto_Criacao_de_Pacotes_em_Python",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)
