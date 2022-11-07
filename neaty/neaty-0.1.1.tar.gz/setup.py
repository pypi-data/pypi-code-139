from distutils.core import setup

import re


def vdk_cleanup(value):
    """
    Remove unexpanded vdk-pylib macros from value
    """

    def has_macro(S):
        return (
            bool(re.match('.*__VDK_PYLIB_[A-Z][A-Z0-9_]__.*', S.strip()))
            or bool(re.match('.*__MKIT_[A-Z][A-Z0-9_]__.*', S.strip()))
        )

    def vdk_cleanup_str(value):
        if has_macro(value):
            return ''
        return value

    def vdk_cleanup_list(value):
        if len(value) == 1:
            if has_macro(value[0]):
                return []
        return value

    if type(value) is str:
        return vdk_cleanup_str(value)
    if type(value) is list:
        return vdk_cleanup_list(value)
    else:
        raise NotImplementedError(f"cannot cleanup: {type(value)}")


long_description = """
__VDK_PYLIB_DESCRIPTION__
"""

requires = [
    '__VDK_PYLIB_REQUIRES_PYSTUFF__',
]

setup(
    description='neaty - Neaty logger',
    license='LGPLv2',
    long_description=vdk_cleanup(long_description),
    maintainer_email='Alois Mahdal <netvor+neaty@vornet.cz>',
    name='neaty',
    packages=['neaty'],
    package_dir={'neaty': 'src/neaty'},
    package_data={'neaty': ['py.typed']},
    url='https://gitlab.com/vornet/python/python-neaty',
    requires=vdk_cleanup(requires),
    version='0.1.1',
)

# setup.py built with MKit 0.0.60 and vdk-pylib-0.0.18+t20221107185540.pt.g3fb8b6a
