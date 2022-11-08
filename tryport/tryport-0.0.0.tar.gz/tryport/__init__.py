import os, sys

def fimport(basename, methodname=None, basename_two=None, level=0):
	"""
	The safe_import function is a helper function that helps to dynamically import modules.
	It is used by the other functions in this file, and it can be used for any python code
	that needs to import modules.  It works by importing the module name given as an argument,
	and if that fails (by raising an ImportError), then it attempts to install the package with:

	Example:
	* abspath = safe_import("os.path", "abspath")
	* rule_mgmt = safe_import("rules", "rule_mgmt", "pysrc.rules")
		* > This will try to import "rules.rule_mgmt"
		* > "rules.rule_mgmt" will fail, so it will try to import "pysrc.rules.rule_mgmt"

	:param basename: Specify the name of the module to import
	:param methodname=None: Specify the name of the class or function to import
	:param basename_two=None: Specify an alternate name to try importing the package as
	:param level=0: Import a module from the current folder
	:return: The output of the __import__ function
	:doc-author: Trelent
	"""
	if basename_two:
		try:
			__import__(basename,level=level)
		except Exception as e:
			basename = basename_two

	try:
		__import__(basename,level=level)
	except Exception as e:
		os.system("{0} -m pip install --upgrade {1}".format(sys.executable, basename.split('.')[0]))

	fromlist = basename.split('.')[1:] if "." in basename else []
	output = __import__(basename,fromlist=fromlist,level=level)

	if methodname:
		output = getattr(output, methodname)

	return output