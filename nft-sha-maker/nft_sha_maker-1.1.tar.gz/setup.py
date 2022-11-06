from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_desc = f.read()

setup(
    name = 'nft_sha_maker',
    version = '1.1',
    author = 'Samuel .O. Bamgbose',
    author_email = 'bsaintdesigns@gmail.com',
    description = ' A package that calculates the SHA256 from a CSV file',
    long_description = long_desc,
    long_description_content_type = 'text/markdown',
    py_modules = ['nft_sha_maker'],
    classifiers = [
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    packages = find_packages(),
    python_requires = '>= 3.10',
    install_requires = [],
    entry_points = {
        'console_scripts' : [
            'nft_sha_maker = nft_sha_maker:__main__',
        ]
    }
)
