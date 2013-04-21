# Gregory Rosenblatt
# 3/15/06

"""Test_Script
	
This is a help message.  Hooray.
"""

from script import Script
import sys


def ListArgs(args):
	print "remaining args:"
	for a in args:
		print a

def TestOpt(arg):
	print "test option:", arg

def SomeOpt():
	print "some option"

main = Script(ListArgs, __doc__, {("t:", "test="): TestOpt
								,("s", "some"): SomeOpt})

if __name__ == "__main__":
	sys.exit(main())
