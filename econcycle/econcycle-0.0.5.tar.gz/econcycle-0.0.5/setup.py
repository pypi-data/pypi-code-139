from setuptools import find_packages, setup  # noqa: H301

NAME = "econcycle"
VERSION = "0.0.5"
REQUIRES = ["finnhub-python==2.4.15"]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name=NAME,
    version=VERSION,
    description="econcycle package",
    author="Sukkwon On",
    author_email="skwon2345@gmail.com",
    url="https://github.com/skwon2345/market-cycle",
    keywords=["econcycle"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
