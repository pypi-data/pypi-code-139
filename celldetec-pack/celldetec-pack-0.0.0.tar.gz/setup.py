from setuptools import setup

def requirements():
	with open("requirements.txt") as f:
		return f.read().splitlines()

setup(
	name="celldetec-pack",
	description="Cell phone detection",
	long_description="README.md",
	packages=["yolov5"],
	python_requires=">=3.6",
	install_requires="requirements.txt"
	)