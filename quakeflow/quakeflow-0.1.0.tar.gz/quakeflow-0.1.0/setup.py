from setuptools import setup

setup(
    name="quakeflow",
    version="0.1.0",
    long_description="quakeflow",
    long_description_content_type="text/markdown",
    packages=["quakeflow"],
    install_requires=["obspy", "h5py", "matplotlib", "pandas"],
)
