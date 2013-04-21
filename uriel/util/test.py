import os
import os.path
import unittest

# recursive walk and grab the test suites from all _Test functions
suites = []
for dir, subdirs, filenames in os.walk(''):
	for fn in filenames:
		name, ext = os.path.splitext(fn)
		if ext in [".py"]:
			module = __import__(name, globals(), locals(), ["_Test"])
			try:
				print name, module
				suites.append(module._Test())
				print "has test"
			except AttributeError:
				pass

# run all the tests
suite = unittest.TestSuite(suites)
unittest.TextTestRunner(verbosity=2).run(suite)
