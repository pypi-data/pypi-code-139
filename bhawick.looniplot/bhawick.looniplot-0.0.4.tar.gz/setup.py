from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="bhawick.looniplot",
    version="0.0.4",
    description="Lightweight plotting to the terminal. 4x resolution via Unicode. This is a fork of Uniplot, please use that library instead.",
    packages=find_packages(include=['looniplot', 'looniplot.*']),
    # py_modules=["looniplot"],
    # package_dir={"": "looniplot"},
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/bhawickjain",
    author="bhawick",
    author_email="53153810+BhawickJain@users.noreply.github.com",

    install_requires = [
        "numpy >= 1.20.0",
    ],

    extras_require = {
        "dev": [
            "pytest >= 3.7",
            "check-manifest",
            "twine",
            "tox",
            "black",
            "flake8",
            "mypy",
            "bump2version",
        ],
    },
)
