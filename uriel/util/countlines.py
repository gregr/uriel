# Gregory Rosenblatt
# 4/12/06

"""Count Lines
	
Counts the number of lines in the given source files.
Usage: python countlines.py [sourcefile1.py sourcefile2.py ...]
	
Example Main options
	-h                     show this help message
"""
import sys
import getopt

class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg

def main(argv=None):
	if argv is None:
		argv = sys.argv
	try:
		# parse command line options
		try:
			opts, args = getopt.getopt(argv[1:], "h", ["help"])
		except getopt.GetoptError, msg:
			raise Usage(msg)
		for o, a in opts:
			if o in ("-h", "--help"):
				print __doc__
				return 0
		# process arguments
		totalLines = 0
		for arg in args:
			currentLines = 0
			for line in open(arg):
				currentLines += 1
				totalLines += 1
			print "%s: %i" % (arg, currentLines)
		print ""
		print "total:", totalLines
	except Usage, err:
		print >>sys.stderr, err.msg
		print >>sys.stderr, "for help use --help"
		return 2

#if __name__ == "__main__":	# maybe this will be useful later
#	sys.exit(main(files))
#else:
import os
import os.path

files = [None]
for d in os.walk(''):
	dir, subs, filenames = d
	for fn in filenames:
		name, ext = os.path.splitext(fn)
		if ext in [".py", ".pyx", ".pxi", ".h", ".cpp"]:
			files.append(os.path.join(dir, fn))
main(files)
