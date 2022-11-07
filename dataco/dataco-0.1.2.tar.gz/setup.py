from codecs import open

from setuptools import setup

requires = [
    "pandas",
    "boto3",
    "google-api-python-client",
    "google-auth-httplib2",
    "google-auth-oauthlib",
]

about = {
    "__description__": "tool to interact with data from different storage services",
    "__author__": "SangDinh",
    "__author_email__": "sxuan29@gmail.com",
    "__url__": "https://github.com/sang-d/data-connector",
}

with open("README.md", "r", "utf-8") as f:
    readme = f.read()

setup(
    name="dataco",
    version="0.1.2",
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    include_package_data=True,
    install_requires=requires,
    package_dir={"dataco": "src"},
    packages=["dataco"],
    python_requires=">=3.4, <4",
)
