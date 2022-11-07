

from distutils.core import setup, Extension

module = Extension('accuModule', sources = ['accumulate.c'])

setup(name = 'accuModule',
          version = '1.0',
          description = 'This is a demo package',
          ext_modules = [module])



