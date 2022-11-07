from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="vihhlima_image_processsing",
    version="0.0.1",
    author="Vitor Lima",
    author_email="vihhlima@hotmail.com",
    description="Image processing package",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vihhlimabr/Image-Processing-Package.git",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)