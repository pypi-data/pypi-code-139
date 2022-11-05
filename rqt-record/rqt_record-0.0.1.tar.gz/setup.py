import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rqt_record",
    version="0.0.1",
    author="daohu527",
    author_email="daohu527@gmail.com",
    description="Cyber record visualization tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/daohu527/rqt_record",
    project_urls={
        "Bug Tracker": "https://github.com/daohu527/rqt_record/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    install_requires=[
        "PyQt5",
        "cyber_record",
    ],
    entry_points={
        'console_scripts': [
            'rqt_record = rqt_record.main:main',
        ],
    },
    python_requires=">=3.6",
)
