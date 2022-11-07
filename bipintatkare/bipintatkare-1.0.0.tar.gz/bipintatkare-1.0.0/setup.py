import setuptools

with open("readme.md", "r") as rd:
    read_file = rd.read()


setuptools.setup(
    name="bipintatkare",
    version="1.0.0",
    author="Bipin Rajesh Tatkare",
    
    description="My sample package to execute",
    long_description=read_file,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    
    python_requires=">=3.6",
    py_modules=["bipintatkare"],
    package_dir={"": "bipintatkare/src"},
    install_requires=[]
)