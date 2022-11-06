import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="morai-kit",
    version="0.0.1",
    author="ischoi",
    author_email="ischoi@morai.ai",
    description="MORAI Sensor Kit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)