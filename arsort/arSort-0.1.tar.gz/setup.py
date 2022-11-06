import setuptools
with open(r'C:\Users\svatoslav\Downloads\arSort\Readme.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='arSort',
	version='0.1',
	author='program_py',
	author_email='semenovsvatoslav19@gmail.com',
	description='a library for lazy people who are too lazy to write their own sorting',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/diarama-py/arSort',
	packages=['arSort'],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)