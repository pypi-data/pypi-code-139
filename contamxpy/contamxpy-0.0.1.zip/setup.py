from __future__ import annotations

import platform
import sys

from setuptools import setup

if platform.python_implementation() == 'CPython':
    try:
        import wheel.bdist_wheel
    except ImportError:
        cmdclass = {}
    else:
        class bdist_wheel(wheel.bdist_wheel.bdist_wheel):
            def finalize_options(self) -> None:
                self.py_limited_api = f'cp3{sys.version_info[1]}'
                super().finalize_options()

        cmdclass = {'bdist_wheel': bdist_wheel}
else:
    cmdclass = {}

setup(
    cffi_modules=['contamxpy_build.py:ffibuilder'], cmdclass=cmdclass,
    data_files=[(
        'lib\\site-packages\\', ["contamx-lib.dll"])],
    project_urls={
        'Web Page': 'https://www.nist.gov/el/energy-and-environment-division-73200/nist-multizone-modeling/',
        'Source': 'https://github.com/usnistgov/contamxpy/',
        },
    
    )
