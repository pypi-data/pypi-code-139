from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "0.0.4"
DESCRIPTION = "Creating machine learning and preprocessing models"
LONG_DESCRIPTION = "A package that allows to process dataset and create classification,clustering and regression models."

# Setting up
setup(
    name="pyautomlib",
    version=VERSION,
    author="nubufi (Numan Burak Fidan)",
    author_email="<numanburakfidan@yandex.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=["numpy", "pandas", "sklearn", "joblib", "xgboost", "lightgbm"],
    keywords=[
        "python",
        "machine learning",
        "clustering",
        "regression",
        "data processing",
        "classification",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
