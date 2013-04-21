# Gregory Rosenblatt
# 12/26/05

from uriel.profiler import settings
import hotshot.stats
import os

# ugly shit
#def Main():
#	import sys
#	"""Execute this module as a statistics-printing script."""
#	if len(sys.argv) > 1:
#		numLines = int(sys.argv[1])
#	else:
#		numLines = 0
#	PrintStats(settings.defaultStatsFile, numLines)

def Print(statsFile, numLines=0, sortParams=settings.defaultSortParams):
	"""Print statistics to stdout in human-readable form."""
	if not os.path.isfile(statsFile):
		print 'The statistics file "%s" does not exist.' % statsFile
		return
	stats = hotshot.stats.load(statsFile)
	stats.strip_dirs()
	stats.sort_stats(*sortParams)
	if numLines > 0:
		stats.print_stats(numLines)
	else:
		stats.print_stats()

#if __name__ == '__main__':
#	Main()
