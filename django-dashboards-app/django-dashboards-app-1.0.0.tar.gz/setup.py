
import setuptools

setuptools.setup(
    name='django-dashboards-app',
    version='1.0.0',
    author='Alberto Sanmartin Martinez',
    author_email='info@albertosanmartinmartinez.es',
    url='https://gitlab.com/albertosanmartinmartinez/django-dashboards',
    license='LICENSE.txt',
    description='Django Dashboard',
    long_description='Django Admin for Developers and Django Dahsboard for Clients',
    install_requires=[
        "django-filter>=22.1",
        "django-widget-tweaks>=1.4.8"
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3"
)