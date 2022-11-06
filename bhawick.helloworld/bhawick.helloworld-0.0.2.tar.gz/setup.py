from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="bhawick.helloworld",
    version="0.0.2",
    description="Say hello!",
    py_modules=["helloworld"],
    package_dir={"": "src"},
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/bhawickjain",
    author="bhawick",
    author_email="53153810+BhawickJain@users.noreply.github.com",

    install_requires = [
        "blessings ~= 1.7",
    ],

    extras_require = {
        "dev": [
            "pytest >= 3.7",
            "check-manifest",
            "twine",
            "tox",
        ],
    },
)
