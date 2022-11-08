from setuptools import setup, find_packages

with open("README.md", encoding='utf-8') as fh:
    long_description = fh.read()

# with open("requirements.txt") as f:
#     required_packages = f.read().splitlines()

setup(
    name="TILM",
    version="0.0.1",
    author="Qingyang Wu",
    author_email="willqywu@gmail.com",
    description="Text-based web interface for language model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=['tilm'],
    # install_requires=required_packages,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
)
