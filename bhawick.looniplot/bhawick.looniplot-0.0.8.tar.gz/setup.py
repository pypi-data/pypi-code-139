from setuptools import setup

setup(
    name="bhawick.looniplot",
    install_requires=[
			"numpy >= 1.20.0", 
    ],
    extras_require={
			"dev": [
					"pytest >= 3.7",
					"check-manifest",
					"twine",
					"tox",
					"black",
					"flake8",
					"mypy",
			],
    },
)