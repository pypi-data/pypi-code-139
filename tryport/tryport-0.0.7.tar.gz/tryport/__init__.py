import os, sys

def fimport(basename, methodname=None, basename_two=None, level=0, basename_lambda=None, install_lambda=None, version=None):
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
	:param methodname=None (str or list): Specify the name of the class or function to import
	:param basename_two=None: Specify an alternate name to try importing the package as
	:param level=0: Import a module from the current folder
	:param basename_lambda: The lambda function to call (no args) if the import fails at basename checking level
	:param install_lambda: The lambda function to call (no args) if the import fails at installation level
	:param version: The version of the program to install
	:return: The output of the __import__ function
	:doc-author: Trelent
	"""
	methodnames = []
	if isinstance(methodname, str):
		methodnames = [methodname]
	elif isinstance(methodname, list):
		methodnames = methodname
	
	full_name = lambda x:x
	if len(methodnames) > 0:
		full_name = lambda x:"{0}.{1}".format(x,methodnames[0])

	if basename_two:
		try:
			try:
				__import__(basename,level=level)
			except:
				if basename_lambda:
					basename_lambda()
				__import__(full_name(basename),level=level)
				__import__(basename,level=level)
		except:
			try:
				__import__(basename_two,level=level)
			except:
				if basename_lambda:
					basename_lambda()
				__import__(full_name(basename_two),level=level)
				__import__(basename_two,level=level)
			basename = basename_two

	try:
		__import__(basename,level=level)
	except Exception as e:
		version_string = "=={0}".format(version) if version else ""
		if install_lambda:
			install_lambda()
		os.system("{0} -m pip install --upgrade {1}{2}".format(sys.executable, basename.split('.')[0], version_string))

	fromlist = basename.split('.')[1:] if "." in basename else []
	output = __import__(basename,fromlist=fromlist,level=level)

	if len(methodnames) > 0:
		return [
			getattr(output, method) for method in methodnames
		]
	else:
		return output