# Gregory Rosenblatt
# 12/26/05

from uriel.profiler.settings import defaultStatsFile
from uriel.profiler import profile, stats

statLines = 50
statSort1 = ('time', 'cum')
statSort2 = ('cum', 'time')

try:
	profile.Run('server.py')
except:
	pass
stats.Print(defaultStatsFile, statLines, statSort1)
stats.Print(defaultStatsFile, statLines, statSort2)
