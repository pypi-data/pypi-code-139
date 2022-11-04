from setuptools import setup

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="dockerode_api_proxy_client",
    version="1.0.0",
    py_modules=["dockerode_api_proxy_client"],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
