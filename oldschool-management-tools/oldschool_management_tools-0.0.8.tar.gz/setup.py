from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="oldschool_management_tools",                     # This is the name of the package
    version="0.0.8",                        # The initial release version
    author="Jim Jimson",                     # Full name of the author
    description="Tools for oldschool managers",
    long_description="Tools for oldschool managers",      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.9',                # Minimum version requirement of the package
    package_dir={'':'src'},     # Directory of the source code of the package
    packages=['oldschool_management_tools', 'oldschool_management_tools.calendar_items', 'oldschool_management_tools.special_prompts'],
    install_requires=["pywin32", "termcolor", "colorama"]              # Install other dependencies if any
)
