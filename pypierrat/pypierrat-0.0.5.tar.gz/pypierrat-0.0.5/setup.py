import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "pypierrat",
    version = "0.0.5",
    author = "JulesPierrat",
    author_email = "jules.pierrat.98@gmail.com",
    description = "Personnal Librairie - Jules Pierrat",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/JulesPierrat/pypierrat",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="./src"),
    python_requires = ">=3.6"
)