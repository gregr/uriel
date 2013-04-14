# Gregory Rosenblatt
# 3/12/06

from perceiver import *
from simulation.awareness import Awareness
from uriel.common.percepts import *
from uriel.core.process import Process
from uriel.core.weakmethod import MethodProxy
from weakref import proxy

class HelloBrain(Awareness):
	def __init__(self, retard):
		Awareness.__init__(self, MethodProxy(self.OnPercepts))
		self.retard = proxy(retard)
		self.entities = set()	# entities already seen
		self.Bind(self.retard.perception)
		self.process = Process(RetardAI(proxy(retard)))
	def OnPercepts(self, percepts):
		for p in percepts:
			type, data = p
			if type == perceptTypes.new_entity:
				space, ident, state = data
				if ident not in self.entities:
					self.entities.add(ident)
					# say hello
					entity = Entity.pool[ident]
					if hasattr(entity, 'name'):
						msg = "hello %s" % entity.name
					else:
						msg = "hello entity number " + str(ident)
					self.retard.OnCommand((Perceiver.actionTypes.talk, (msg,)))

def RetardAI(retard):
	moves = [0, 1, 2, 3]	# yes, it is pointless as it is
#	moves = [((0,-1,0), 0), ((1,0,0), 1), ((0,1,0), 2), ((-1,0,0), 3)]
	messages = ["I hate all life.",
				"Why do I exist?",
				"Kill kill kill kill...",
				"DIE DIE DIE!"
				]
	step = 0
	state = 0
	interval = 100
	while True:
		if step >= interval:
			step -= interval
			direction = moves[state]
			msg = messages[state]
			if state == 3:
				state = -1
			state += 1
			retard.OnCommand((Perceiver.actionTypes.orient, (direction,)))
			retard.OnCommand((Perceiver.actionTypes.move, (direction,)))
#			retard.OnCommand((serverCommands.talk, (msg,)))
		step += 1
		yield None
