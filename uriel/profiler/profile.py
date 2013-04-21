# Gregory Rosenblatt
# 12/26/05

from uriel.profiler import settings
import hotshot

# this is the ugliest shit in the world... almost
#def Main():
#	import sys
#	"""Execute this module as a profiling script."""
#	if len(sys.argv) != 2:
#		print 'Incorrect number of commandline arguments provided.'
#		print '1 expected: scriptName'
#		sys.exit(1)
#	ProfileScript(sys.argv[1])

def Run(scriptName, statsFile=settings.defaultStatsFile):
	"""Profile the given script and output the statistics to file."""
	p = hotshot.Profile(statsFile)
	runString = 'execfile("%s")' % scriptName
	p.run(runString)

#if __name__ == '__main__':
#	Main()
