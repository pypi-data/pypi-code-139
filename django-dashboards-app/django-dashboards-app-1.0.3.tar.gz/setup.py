
import os
import sys
import setuptools

__version__ = "1.0.3"

f = open("README.rst")
readme = f.read()
f.close()


if sys.argv[-1] == "publish":
    if os.system("pip freeze | grep wheel"):
        print("wheel not installed.\nUse `pip install wheel`.\nExiting.")
        sys.exit()
    if os.system("pip freeze | grep twine"):
        print("twine not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    #print("You probably want to also tag the version now:")
    #print("  git tag -a %s -m 'version %s'" % (__version__, __version__))
    #print("  git push --tags")
    sys.exit()

setuptools.setup(
    name="django-dashboards-app",
    version=__version__,
    description="Django Admin for Developers and Django Dahsboards for Clients",
    long_description=readme,
    author="Alberto Sanmartin Martinez",
    author_email="info@albertosanmartinmartinez.es",
    maintainer="Alberto Sanmartin Martinez",
    maintainer_email="info@albertosanmartinmartinez.es",
    url="https://gitlab.com/albertosanmartinmartinez/django-dashboards",
    packages=setuptools.find_packages(exclude=["tests*"]),
    license="GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Natural Language :: English",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Topic :: Software Development :: Libraries :: Application Frameworks"
    ],
    zip_safe=False,
    python_requires=">=3",
    install_requires=[
        "Django>=3",
    ],
)