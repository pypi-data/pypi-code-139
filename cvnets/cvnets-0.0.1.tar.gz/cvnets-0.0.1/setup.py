import os
import setuptools

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

setuptools.setup(
    name="cvnets",
    version="0.0.1",
    author="Jihoon Lucas Kim",
    description="Library for Computer Vision Deep Learning Networks",
    packages=["cvnets"]
)