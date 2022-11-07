from setuptools import setup

version = "1.0.0"

with open("README.md") as f:
    readme = f.read()

with open("requirements.txt") as f:
    requirements = f.read().split("\n")

setup(
    name="alt-discord-flags-v2",
    author="Circuit, MoonlightCapital",
    version=version,
    url="https://github.com/MoonlightCapital/Flag-Parsing",
    packages=['discord.ext.flags'],
    license='MIT',
    description="A Discord.py extension allowing you to pass flags as arguments.",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=requirements,
    extras_require=None,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ]
)
