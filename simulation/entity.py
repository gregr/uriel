# Gregory Rosenblatt
# 2/10/06

from signals import *
from uriel.core.struct import Struct
from weakref import WeakValueDictionary, ref


class Entity(object):
	"""A basic simulation object that maintains its own state."""

	#__slots__ = ["_spaceref", "externalState", "__weakref__"]

	pool = WeakValueDictionary()

	mediums = []

	def __init__(self, location, type, **externalState):
		"""Create an entity at the given location with specified properties.
			
		location - a tuple containing a space, sector pair
		type - describes the classification the entity belongs to
		externalState - a list of key, value pairs describing visible state
		"""
		Entity.pool[id(self)] = self
		space, sector = location
		self._spaceref = ref(space)	# prevent circular referencing
		self.externalState = Struct(type=type, sector=sector, **externalState)
		space[sector].AddEntity(self)
		space.OnSignal(NewEntitySignal(self.mediums, self))

	def Destroy(self):
		"""Force destruction of an entity by eliminating spatial references.
			
		For specialized destruction behavior, this should be extended.
		Extending methods should probably call this at the end.
		Use __del__ to specify normal cleanup behavior.
		"""
		space = self.space
		sector = self.sector
		assert space[sector]
		space[sector].RemoveEntity(self)
		space.OnSignal(DelEntitySignal(self.mediums, self, sector))

	def ChangeExternalState(self, field):
		"""Change the value of a given external state variable."""
		var, value = field
		self.externalState.__dict__[var] = value
		space = self.space
		space[self.sector].OnStateChange()
		space.OnSignal(EntityStateChangeSignal(self.mediums, self, field))

	def ChangeSector(self, sector):
		"""Move the entity to a new sector."""
		assert sector != self.sector
		space = self.space
		space[sector].AddEntity(self)
		space[self.sector].RemoveEntity(self)
		oldsector = self.sector
		self.externalState.sector = sector
		space.OnSignal(DepartSignal(self.mediums, self, oldsector))
		space.OnSignal(ArriveSignal(self.mediums, self, oldsector))

	def ChangeSpace(self, location):
		"""Move the entity to a completely new spatial location."""
		space, sector = location
		oldspace, oldsector = self.space, self.sector
		assert space != oldspace
		space[sector].AddEntity(self)
		oldspace[oldsector].RemoveEntity(self)
		self._spaceref, self.externalState.sector = ref(space), sector
		oldspace.OnSignal(DelEntitySignal(self.mediums, self, oldsector))
		space.OnSignal(NewEntitySignal(self.mediums, self))

	space = property(lambda self: self._spaceref())
	sector = property(lambda self: self.externalState.sector)
	state = property(lambda self: self.externalState.__dict__)
