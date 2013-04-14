# Gregory Rosenblatt
# 3/23/06

from signals import *
from uriel.core.struct import Struct

# light (illumination) as a resource?
class Sector(object):
	"""The granular spatial element describing a position.
		
	Contains a dictionary of resources {type: amount} as well as
	a list of the entities present at this location.
	"""

	__slots__ = ["entities", "terrain", "resources", "_stateId"]

	def __init__(self):
		"""Create a sector containing the given resources."""
		self.entities = set()
		self.terrain = None	# sand, soil, water, air, etc.
		self.resources = {}	# mineral or other compositions
		self._stateId = 0	# incremented whenever visible state changes

	def OnStateChange(self):
		"""Designate a state change for this sector."""
		self._stateId += 1

	def _GetStateId(self):
		if (not self.entities) and (not self.terrain):
			return None		# designate an empty sector
		return self._stateId

	stateId = property(_GetStateId)

	def AddEntity(self, entity):
		"""Add an entity to this sector."""
		self.entities.add(entity)
		self.OnStateChange()

	def RemoveEntity(self, entity):
		"""Remove an entity from this sector."""
		self.entities.remove(entity)
		self.OnStateChange()


class Space:
	"""A collection of indexed sectors describing a spatial environment."""

	def __init__(self, signalHandlers):
		"""Create a space which supports the given signal handlers."""
		self.signalHandlers = signalHandlers

	def __getitem__(self, index):
		"""Retrieve a sector using an appropriate index."""
		raise NotImplementedError

	def OnSignal(self, signal):
		"""Propogate a signal with the appropriate handler."""
		mediums, data, sectors = signal
		data.append(set())	# for tracking who has already handled this signal
		for m in mediums:
			self.signalHandlers[m].OnSignal(data, sectors)


class AssociationSpace(Space):
	"""A space which behaves like a dictionary of sectors."""

	def __init__(self, signalHandlers, indices, sectorType=Sector):
		"""Create a space containing sectors with the given indices."""
		Space.__init__(self, signalHandlers)
		self.sectors = dict((i, sectorType()) for i in indices)

	def __getitem__(self, index):
		"""Retrieve a sector via association index."""
		return self.sectors[index]


class Array3dSpace(Space):
	"""A space with its sectors arranged as a 3-dimensional array."""

	def __init__(self, signalHandlers, size, sectorType=Sector):
		"""Create a space with the three dimensions given in size."""
		Space.__init__(self, signalHandlers)
		self.size = size
		width,height,depth = size
		self.sectors = [[[sectorType() for i in xrange(width)]
								for j in xrange(height)]
							for k in xrange(depth)]

	def __getitem__(self, index):
		"""Retrieve a sector by coordinate index."""
		i,j,k = index
		if (i < 0) or (j < 0) or (k < 0):
			raise KeyError
		return self.sectors[k][j][i]


# add __init__ containing a sectorType with terrain
class TerrainSpace(Array3dSpace):
	"""A space describing a world made up of sectors that include terrain."""

	mediums = []	# medium transmission for terrain change signals

	def SetTerrain(self, sector, terrain):
		"""Set the terrain for the given sector."""
		s = self[sector]
		s.terrain = terrain
		s.OnStateChange()
		self.OnSignal(TerrainChangeSignal(self.mediums, sector, terrain))

	def SetResource(self, sector, resource):
		"""Set the specified resource for this sector.
			
		The resource argument is a (name, value) pair describing the resource.
		"""
		name, value = resource
		s = self[sector]
		if not value:
			if name in s.resources:
				del s.resources[name]
			else:
				return
		else:
			s.resources[name] = value
		# change terrain based on resource change (if necessary) right here
		# use some kind of resource -> terrain table...

## TODO ##

class PhonySpace:
	sector = Struct(OnStateChange=lambda:None
						,AddEntity=lambda _:None
						,RemoveEntity=lambda _:None)
	def __getitem__(self, index):
		return self.sector
	def OnSignal(self, signal):
		pass


class Container:
	space = PhonySpace()
	def __init__(self, slots):
		self.slots = dict((s, None) for s in slots)
	def __getitem__(self, slot):
		return self.slots[slot]
	def __setitem__(self, slot, entity):
		self.slots[slot] = entity
		entity.ChangeSpace((self.space, slot))
	def __delitem__(self, slot):
		self.slots[slot] = None
	def Dump(self, slot, destination):
		self[slot].ChangeSpace(destination)
		del self[slot]
