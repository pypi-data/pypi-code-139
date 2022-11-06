import setuptools
    
    
    
setuptools.setup(
    name="asyncytmusicapi",
    version="1.7",
    license='MIT',
    author="sheldy",
    description="Unofficial youtube music API",
    url="https://github.com/sheldygg/asyncytmusicapi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"
    ],
    install_requires=[
        'aiohttp'
    ],
)