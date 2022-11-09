import os
import re
import sys
import subprocess
from setuptools import setup
from setuptools import find_packages


def read_version():
    regexp = re.compile(r"^__version__\W*=\W*'([\d.abrc]+)'")
    init_py = os.path.join(os.path.dirname(__file__), "polaris", "__init__.py")
    if sys.version.startswith('2'):
        ver = init_py.replace("__init__.py", "version.2")
    else:
        ver = init_py.replace("__init__.py", "version.3")
    subprocess.Popen([sys.executable, ver], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    with open(init_py) as f:
        for line in f:
            match = regexp.match(line)
            if match is not None:
                return match.group(1)
        raise RuntimeError("Cannot find version in {}".format(init_py))


setup(
    name="polaris-python",
    version=read_version(),
    description="polaris Python SDK",
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.27.1"
    ],
    packages=find_packages(include=("polaris", "polaris.*"))
)
