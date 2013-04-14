# Gregory Rosenblatt
# 1/22/06

from weakref import WeakValueDictionary

def AgentUpdater():
	"""Execute the programs of all existing agents."""
	while True:
		for m in Agent.pool.values():
			if m.percepts:
				m.program(m.percepts)	# call the program with percept input
				m.percepts = []			# clear the queue
		m = None	# don't imprison references in this generator
		yield None


class Agent(object):
	"""Program that interacts with the simulation taking percepts as inputs."""

	pool = WeakValueDictionary()

	def __init__(self, program):
		"""Create an agent for the given program."""
		Agent.pool[id(self)] = self
		self.program = program
		self.percepts = []
