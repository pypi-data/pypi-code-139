import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='bvlain',  
     version='0.1',
     py_modules = ["bvlain"],
     install_requires = ["numpy",
                         "pandas",
                         "scipy",
                         "networkx",
                         "pymatgen",
                         "ase"],
     author="Artem Dembitskiy",
     author_email="art.dembitskiy@gmail.com",
     description="The Bond valence site energy calculator",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/dembart/BVlain",
     package_data={"bvlain": ["*.txt", "*.rst","*"], 'tests':['*'], '':['bvlain/data/*.pkl'], 'pixmaps':['.png'], '':['*']},
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
    include_package_data=True,
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where="src"),
 )


