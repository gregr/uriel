# Gregory Rosenblatt
# 1/22/06

from time import clock

class Timer:
	def __init__(self, clockfunc=clock):
		self.current = clockfunc()
		self.clock = clockfunc
	def __call__(self):
		next = self.clock()
		delta = next - self.current
		self.current = next
		return delta
