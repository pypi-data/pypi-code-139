import setuptools

setuptools.setup(
    name="software1checker",
    version="0.0.3",
    author="Noam Zaks",
    description="A test runner for the software 1 course",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    py_modules=["software1checker"],
    package_dir={"": "software1checker"},
    install_requires=[],
    entry_points={
        "console_scripts": [
            "software1checker = software1checker.main:main",
        ],
    },
)
