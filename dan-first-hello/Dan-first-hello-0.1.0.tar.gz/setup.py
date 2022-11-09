from setuptools import setup
setup(
    name="Dan-first-hello",
    version="0.1.0",
    author="Dan Ciuban",
    author_email="danciuban@outlook.com",
    packages=["my_own_package"],
    package_dir={"": "src\\"},
    include_package_data=True
)