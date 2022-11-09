from time import time
import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="liuyuanlin",
    version="2.0.1",
    author="liuyuanlin",
    author_email="liuyuanlins@outlook.com",
    description="This is a gift for liumenghan.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MisakaMikoto128/liuyuanlin",
    project_urls={
        "Bug Tracker": "https://github.com/MisakaMikoto128/liuyuanlin/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'liuyuanlin = liuyuanlin:liuyuanlin',
        ]
    },
    package_dir={"": "src"},

    install_requires=["numpy>=1.20.1","opencv-python>=4.5.1.48"],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
