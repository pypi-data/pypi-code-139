from setuptools import setup, find_packages

setup(
    name="ori_optimize",
    version="0.1.0",
    description="a environment that controls STL model rotate to reach the maximal 3D printing quality.",
    install_requires=["gym==0.25.2", "numpy"],
    packages=find_packages()
)
