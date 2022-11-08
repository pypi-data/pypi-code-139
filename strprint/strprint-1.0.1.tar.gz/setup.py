from setuptools import setup, find_packages

setup(
    name="strprint",
    version="1.0.1",
    packages=find_packages(),
    description='str print',
    author='lixianyang',
    include_package_data=True, 
    package_data={
        'strprint': ['*.so'] #会将对应文件打包，也可以通过MANIFEST.in文件来实现include str_print/libstr_print_c_warpper.so

    },
)