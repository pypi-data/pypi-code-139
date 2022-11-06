import setuptools

# use src.ppcmd.*, ppcmd.* cause ModuleNotFoundError: No module named 'ppcmd'
from src.ppcmd.ppc.version import __version__

setuptools.setup(
    name="ppcmd",
    version=__version__,
    include_package_data=True,
    package_dir={"": "src"},
    packages=setuptools.find_namespace_packages(where="src", include=["*"]),
    python_requires=">=3.8",
    install_requires=[
        "click == 8.1.3",
        "colorama == 0.4.6",
        "pygit2 == 1.10.1",
    ],
    entry_points="""
        [console_scripts]
        ppc=ppcmd.ppc.ppc:cli
    """,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
