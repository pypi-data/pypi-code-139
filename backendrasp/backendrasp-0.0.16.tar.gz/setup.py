from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup_args = dict(
    name='backendrasp',
    version='0.0.016',
    packages=find_packages(),
    author="Shivam Sharma",
    author_email="shivamsharma1913@gmail.com",
    description="Shyna Backend Functionality Package For Rasp",
    long_description=long_description,
    long_description_content_type="text/markdown",
)

install_requires = [
    "setuptools",
    "wheel",
    'ShynaTime',
    'ShynaDatabase',
    'nltk',
    'requests',
    'face_recognition',
    'googlesearch-python',
    'wikipedia',
    'IMDbPY',
    'wget',
    'telegram',
    'feedparser',
    'google_speech',
    'haversine'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
