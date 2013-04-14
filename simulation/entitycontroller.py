# Gregory Rosenblatt
# 3/10/06

from uriel.core.process import ProcessGroup, Process
from weakref import ref, proxy


class EntityController(object):
	"""Interface for controlling an entity remotely.
		
	For an entity to receive actions, it must define:
		OnAction(data) -- where data is a tuple (type, args)
	"""

	def __init__(self, entity):
		"""Create a controller for the given entity and its actions."""
		ProcessGroup(self)
		self._entityref = ref(entity)
		self.actionQueue = {}
		# do not create a zombie controller
		self.process = Process(self.__class__.Executer(proxy(self)))
		#self.process.process.next()	# make sure proxy is installed

	def OnAction(self, type, args):
		"""Queue up an action and its arguments for processing."""
		self.actionQueue[type] = args

	def Executer(self):
		"""Execute queued actions during the simulation process loop.
			
		When a sufficient number of simulation steps have elapsed, an action
		is popped off the queue and called through the entity's interface.
		"""
#		self = proxy(self)	# do not create a zombie controller
#		yield None	# end of proxy installation
		while True:
			self.updater.next()
			onAction = self.entity.OnAction
			queue = self.actionQueue
			for data in queue.copy().iteritems():	# queue
				type, args = data
				onAction(type, args)
#				print "calling:", type
				del queue[type]
			onAction = None
			queue = None
			yield None

	def CoolOffProcess(self, attrName, callback=lambda:None):
		"""Increment a cooloff counter until it reaches the delay threshold.
			
		A callback may be triggered once the cooloff period completes.
		"""
		entity = proxy(self.entity)
		del self	# anti-zombie
		cooloff = attrName + "CoolOff"
		delay = attrName + "Delay"
		while getattr(entity, cooloff) < getattr(entity, delay):
			setattr(entity, cooloff, getattr(entity, cooloff)+1)
			print "updating:", cooloff, getattr(entity, cooloff)
			yield None
		delattr(entity, cooloff)
		callback()

	def StartCoolOff(self, attrName):
		entity = self.entity
		proc = self.__class__.CoolOffProcess(proxy(self), attrName)
		#proc.next()	# initialization
		setattr(entity, attrName+"CoolOff", 0)
		setattr(entity, attrName+"CoolOffProcess", Process(proc, self))

	def CallAfterCoolOff(self, attrName, callback):
		entity = self.entity
		if hasattr(entity, attrName+"CoolOff"):
			proc = self.__class__.CoolOffProcess(proxy(self), attrName
												,callback)
			#proc.next()	# intitialization
			setattr(entity, attrName+"CoolOffProcess", Process(proc, self))
		else:
			callback()

	entity = property(lambda self: self._entityref())
