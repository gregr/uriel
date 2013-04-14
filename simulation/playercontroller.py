# Gregory Rosenblatt
# 3/5/06

from awareness import Perspective
from uriel.common.percepts import perceptTypes
from uriel.core.weakmethod import MethodProxy
from uriel.core.functionmap import MakeFunctionMap
from uriel.core.enum import Enum
from weakref import ref, WeakKeyDictionary


class PlayerController(object):
	""""""

	commandTypes = Enum(["test"])

	def __init__(self, awareness, entity):
		self.awareness = awareness
		self.Bind(entity)	# eventually an entity won't be bound right away

	def __del__(self):
		entity = self.entity
		del self._entityref
		entity.Destroy()	# later, disconnecting won't destroy the entity?

	def Bind(self, entity):
		onDestroyed = MethodProxy(self.OnEntityDestroyed)
		self._entityref = ref(entity, lambda _: onDestroyed())
		totalNames = entity.actionTypes.names + self.commandTypes.names
		self.awareness.percepts.append((perceptTypes.new_commands
										,totalNames))
		self.altPerspectives = WeakKeyDictionary()
		self.mainPerspective = Perspective(self.awareness, entity.perception)
#		self.awareness.Bind(entity.perception)

	# this won't be necessary?
	def OnEntityDestroyed(self):	# eventually this will be first
		self.awareness.percepts.append((perceptTypes.new_commands
										,self.commandTypes.names))

	def AddPerspective(self, perception):	# later, add a default command
		self.altPerspectives[perception] = Perspective(self.awareness
													,perception)

	def RemovePerspective(self, perception):	# and a command for this
		try:
			del self.altPerspectives[perception]
		except KeyError:
			pass

	commands, commandhandler = MakeFunctionMap()

	def OnCommand(self, data):
		type, args = data
		entity = self.entity
		if type < entity.actionTypes.numVals:
			entity.OnCommand(data)
		else:	# this crap will be part of its own commandable entity
			type -= entity.actionTypes.numVals
			if type in self.commands:
				self.commands[type](self, *args)

	@commandhandler(commandTypes.test)
	def OnTest(self, crap):
		print "testing default command:", crap

	entity = property(lambda self: self._entityref())
