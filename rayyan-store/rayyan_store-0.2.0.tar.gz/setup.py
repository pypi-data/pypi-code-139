from setuptools import setup

requirements = ['requests']

setup(
    name="rayyan_store",
    version="0.2.0",
    description="Python client interface for RayyanStore",
    author="Fadhil Abubaker",
    packages=['rayyan_store'],
    install_requires=requirements
)
