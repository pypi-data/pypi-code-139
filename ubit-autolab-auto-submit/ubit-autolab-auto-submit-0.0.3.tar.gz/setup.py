import setuptools

reqs = ['selenium==4.5.0', 'webdriver_manager==3.8.4', 'packaging==21.3', 'ubit-autolab-commit-parser']

setuptools.setup(
    name='ubit-autolab-auto-submit',
    version='0.0.3',
    description='Automated AutoLab Submissions',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    python_requires='>=3.6, <4',
    install_requires=reqs
)
