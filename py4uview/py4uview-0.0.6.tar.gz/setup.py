from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="py4uview",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    author="Lin Zhu",
    author_email="lin.zhu@maxiv.lu.se",
    description="Data analysis package for MAXPEEM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.maxiv.lu.se/zhulin/py4uview",
    project_urls={
        "Bug Tracker": "https://gitlab.maxiv.lu.se/zhulin/py4uview/-/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=["numpy", "matplotlib", "scipy", "xarray"],
    python_requires=">=3.9",
)
