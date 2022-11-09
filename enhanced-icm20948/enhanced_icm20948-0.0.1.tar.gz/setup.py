import sys
from glob import glob
from pybind11 import get_cmake_dir
from pybind11.setup_helpers import Pybind11Extension, build_ext
from pybind11.setup_helpers import ParallelCompile, naive_recompile
from setuptools import setup

__version__ = '0.0.1'

ext_modules = [
    Pybind11Extension(
        "enhanced_icm20948.asm_orientation",
        sorted(glob("enhanced_icm20948/asm_orientation/*.cpp"))
    )
]

ParallelCompile("NPY_NUM_BUILD_JOBS", needs_recompile=naive_recompile).install()

setup(
    name = "enhanced_icm20948",
    version = __version__,
    author = "Haoyuan Ma",
    author_email = "mhy@flyinghorse.top",
    license = "MIT",
    url = "https://gogs.infcompute.com/",
    description = "A test project using pybind11 & I2C",
    long_description = "https://gogs.infcompute.com/",
    ext_modules = ext_modules,
    cmdclass = {"build_ext": build_ext},
    zip_safe = False,
    python_requires = ">=3.7",
    packages = ["enhanced_icm20948"],
    install_requires = [
        'numpy'
    ]
)