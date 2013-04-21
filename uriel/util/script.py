# Gregory Rosenblatt
# 3/15/06

import sys
import getopt


class UsageError(Exception):
	def __init__(self, msg):
		self.msg = msg


class Script:
	def __init__(self, program, helpMsg="", optionHandlers={}):
		self.program = program
		def OnHelp():
			print helpMsg
			return 0
		optionHandlers[("h", "help")] = OnHelp
		self.handlers = {}
		self.options = []
		self.longOptions = []
		for key, handler in optionHandlers.iteritems():
			o, lo = key
			if o:
				self.options.append(o)
				if o[len(o)-1:len(o)] == ":":
					o = o[:len(o)-1]
				self.handlers["-"+o] = handler
			if lo:
				self.longOptions.append(lo)
				if lo[len(lo)-1:len(lo)] == "=":
					lo = lo[:len(lo)-1]
				self.handlers["--"+lo] = handler
	def __call__(self, argv=None):
		if argv is None:
			argv = sys.argv
		try:
			# parse command line options
			try:
				opts, args = getopt.getopt(argv[1:], "".join(self.options)
											,self.longOptions)
			except getopt.GetoptError, msg:
				raise UsageError(msg)
			# handle options
			for o, a in opts:
				h = self.handlers[o]	# this should always succeed...
				if a:
					result = h(a)
				else:
					result = h()
				if result is not None:
					return result
			# run program on remaining args
			self.program(args)
		except UsageError, err:
			print >>sys.stderr, err.msg
			print >>sys.stderr, "for help use --help"
			return 2


# usage example:
#if __name__ == "__main__":
#	main = Script(program, msg, options)
#	sys.exit(main())
