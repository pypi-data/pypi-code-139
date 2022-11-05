from setuptools import find_packages, setup,find_namespace_packages


print(find_namespace_packages(where='src'))
setup(
   name='nanoyc-logging',
   version='0.1.0',
   author='Dima Frolenko',
   author_email='orangefrol@gmail.com',
   packages=find_namespace_packages(where='src'),
   package_dir={"": "src"},
#    entry_points = {
#         'console_scripts': ['nf=nf_lite.command_line:main'],
#    },
   license='LICENSE.txt',
   description='A nano package for working with Yandex Cloud',
   long_description=open('README.txt').read(),
   long_description_content_type='text/plain',
   install_requires=open('requirements.txt').readlines()
)