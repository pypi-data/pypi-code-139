import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pypierrat",
    version="0.0.3",
    author="Jules Pierrat",
    author_email="jules.pierrat.98@gmail.com",
    description="My Personal Python Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JulesPierrat/pypierrat",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)