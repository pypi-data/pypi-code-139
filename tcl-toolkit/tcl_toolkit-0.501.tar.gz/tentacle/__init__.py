# !/usr/bin/python
# coding=utf-8
import sys, os.path


name = 'tcl_toolkit'
__version__ = '0.501'


def greeting(hello=False, mod_version=False, py_version=False):
	'''
	'''
	if hello: #print greeting
		import datetime
		hour = datetime.datetime.now().hour
		greeting = 'morning' if 5<=hour<12 else 'afternoon' if hour<18 else 'evening'
		print('Good {}!'.format(greeting))

	if py_version: #print python version
		print ('You are using python interpreter v{}.{}.{}'.format(sys.version_info[0], sys.version_info[1], sys.version_info[2]))

	if mod_version:
		print ('Loading Tentacle v{} ..'.format(__version__))


def appendPaths(verbose=False, exclude=[]):
	'''Append all sub-directories to the python path.

	:Parameters:
		exclude (list) = Exclude directories by name.
		verbose (bool) = Output the results to the console. (Debug)
	'''
	path = (__file__.rstrip(__file__.split('\\')[-1])) #get the path to this module, and format it to get the path root.

	sys.path.insert(0, path)
	if verbose:
		print (path)

	# recursively append subdirectories to the system path.
	for root, dirs, files in os.walk(path):
		for dir_name in dirs:
			if not any([(e in root or e==dir_name) for e in exclude]):
				dir_path = os.path.join(root, dir_name)
				sys.path.insert(0, dir_path)
				if verbose:
					print (dir_path)


def lazy_import(importer_name, to_import):
	'''Return the importing module and a callable for lazy importing.

	:Parmameters:
		importer_name (str) = Represents the module performing the
				import to help facilitate resolving relative imports.
		to_import (list) = An iterable of the modules to be potentially imported (absolute
				or relative). The 'as' form of importing is also supported. e.g. 'pkg.mod as spam'
	:Return:
		(tuple) (importer module, the callable to be set to '__getattr__')

	ex. call: 	path = os.path.abspath(os.path.dirname(__file__))
				subpackages = [f.path for f in os.scandir(path) if f.is_dir() and not f.name.startswith('_')]
				mod, __getattr__ = lazy_import(__name__, subpackages)
	'''
	module = importlib.import_module(importer_name)
	import_mapping = {}
	for name in to_import:
		importing, _, binding = name.partition(' as ')
		if not binding:
			_, _, binding = importing.rpartition('.')
		import_mapping[binding] = importing

	def __getattr__(name):
		if name not in import_mapping:
			message = f'module {importer_name!r} has no attribute {name!r}'
			raise AttributeError(message)
		importing = import_mapping[name]
		# imortlib.import_module() implicitly sets submodules on this module as appropriate for direct imports.
		imported = importlib.import_module(importing, module.__spec__.parent)
		setattr(module, name, imported)

		return imported

	return module, __getattr__


greeting(hello=1, mod_version=1, py_version=1)
appendPaths(verbose=0)









# -----------------------------------------------
# Notes
# -----------------------------------------------


# -----------------------------------------------
# deprecated:
# -----------------------------------------------