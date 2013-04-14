# Gregory Rosenblatt
# 3/4/06

from sensor import Sensor
from signals import *
from uriel.common.percepts import *
from uriel.core.weakmethod import MethodProxy
from uriel.core.functionmap import MakeFunctionMap
from uriel.core.tuplemath import IntegerScale3d as ScaleSector
from uriel.core.tuplemath import Mod3d as ModSector
from weakref import ref, proxy, WeakValueDictionary

# use this to figure out what a perception can view (line of sight)
def GetRegionsInRange(space, sector, range, scale):
	if scale == 1:
		width, height, depth = space.size
		x,y,z = sector
	else:
		factor = 1.0/scale
		range = int(range * factor)
		width, height, depth = ScaleSector(space.size, factor)
		mw, mh, md = ModSector(space.size, scale)
		width += int(bool(mw))
		height += int(bool(mh))
		depth += int(bool(md))
		x,y,z = ScaleSector(sector, factor)
	rangeplusone = range+1
	regions = set()
	for k in xrange(max(0, z-range), min(depth, z+rangeplusone)):
		for j in xrange(max(0, y-range), min(height, y+rangeplusone)):
			for i in xrange(max(0, x-range), min(width, x+rangeplusone)):
				regions.add((i,j,k))
	return regions

def GetSectorsInRegions(regions, scale):
	if scale == 1:
		return regions
	for r in regions:
		x,y,z = r
		sectors = set()
		for k in xrange(scale):
			for j in xrange(scale):
				for i in xrange(scale):
					sectors.add((x+i, y+j, z+k))
	return sectors

class Perception(object):
	pool = WeakValueDictionary()
	def __init__(self, entity, senses, detectionMediums):
		Perception.pool[id(self)] = self
		self._entityref = ref(entity)
		self.awarenesses = set()
		space = entity.space
		self._spaceref = ref(space)
		self.sensors = {}
		# using this will avoid circular references
		onSignal = MethodProxy(self.OnSignal)
		for t in senses:
			try:	# change requirements so that this should always succeed
				self.sensors[t] = (Sensor(space.signalHandlers[t]
											,onSignal)
								,senses[t])
			except KeyError:
				pass	# handle the space's lack of signal support for t
		self.detectionMediums = set(detectionMediums)
		self.sectors = set()
#		self.viewedSectors = set()
		self.ChangeSector(entity.sector)
	def __del__(self):
		awarenesses = self.awarenesses.copy()
		for a in awarenesses:
			a().Unbind(self)
#		for (s, r) in self.sensors.values():
#			s.Destroy()
	def ChangeSector(self, sector):
		space = self.space
		for t in self.sensors:
			sensor, range = self.sensors[t]
			sensorMap = space.signalHandlers[t]
			scale = sensorMap.regionSize
			sensor.ListenTo(GetRegionsInRange(space, sector, range, scale))
		# any new sectors and entities should be added to update
		sectors = set()
		for m in self.detectionMediums:
			sectors |= self.sensors[m][0].regions # factor in regionsize later
		added = sectors - self.sectors
		for a in self.awarenesses:
			self._Update(a(), added)
		self.sectors = sectors#.copy()
	def ChangeSpace(self, location):
		space, sector = location
		self._spaceref = ref(space)
		self.sectors = set()
		# todo: send update about change of spaces (not necessary now?)
		for t in self.sensors:
			try:	# see above
				self.sensors[t][0].ChangeMap(space.signalHandlers[t])
			except KeyError:
				pass# use null map that never gets signals (class member)
		self.ChangeSector(sector)
	def AttachAwareness(self, awareness):
		self.awarenesses.add(ref(awareness, self.awarenesses.remove))
		# id of space should be included in identity percept, for organization
		awareness.percepts.append((perceptTypes.new_identity
									,id(self.entity)))
		self._Update(awareness, self.sectors)	# all sectors
	def DetachAwareness(self, awareness):
		awareness.percepts.append((perceptTypes.del_identity
									,id(self.entity)))
		self.awarenesses.remove(ref(awareness))
	def _UpdateViewState(self, sector):
		space = self.space
		stateId = space[sector].stateId
		for a in self.awarenesses:
			a().SetViewState(space, sector, stateId)
	def _Update(self, awareness, sectors):
		newSectors = []
		newEntities = []
		space = self.space
		detectionMediums = self.detectionMediums
		for s in sectors:
			sector = space[s]
			state = awareness.GetViewState(space, s)
			stateId = sector.stateId
			if state == stateId:
				continue
			# otherwise send necessary data
			awareness.SetViewState(space, s, stateId)
			entities = []
			for e in sector.entities:
				if detectionMediums.intersection(e.mediums):
					newEntities.append((id(e), e.state.copy()))
			newSectors.append((s, sector.terrain))
		if newSectors:
			newSectors.append(id(space))
			awareness.percepts.append((perceptTypes.new_sector_group
										,newSectors))
		if newEntities:
			newEntities.append(id(space))
			awareness.percepts.append((perceptTypes.new_entity_group
										,newEntities))

	# signal handling
	signalHandlers, signalhandler = MakeFunctionMap()

	def OnSignal(self, signal):
		type, data, handled = signal
		percept = self.signalHandlers[type](self, data)
		for a in (self.awarenesses - handled):
			a().percepts.append(percept)
			handled.add(a)

	@signalhandler(signalTypes.terrain_change)
	def OnTerrainChange(self, data):
		sector, terrain = data
		self._UpdateViewState(sector)
#		self.viewedSectors.add(self.entity().space()[sector])
		return (perceptTypes.terrain_change
				,(id(self.space), sector, terrain))

	@signalhandler(signalTypes.new_entity)
	def OnNewEntity(self, entity):
		self._UpdateViewState(entity.sector)
#		self.viewedSectors.add(entity.space()[entity.sector])
		return (perceptTypes.new_entity
				,(id(entity.space), id(entity), entity.state.copy()))

	@signalhandler(signalTypes.del_entity)
	def OnDelEntity(self, data):
		entity, oldpos = data
		self._UpdateViewState(oldpos)
		return (perceptTypes.del_entity, id(entity))

	@signalhandler(signalTypes.depart)
	def OnDepart(self, data):
		entity, oldpos = data
		self._UpdateViewState(oldpos)
		return (perceptTypes.depart, id(entity))

	@signalhandler(signalTypes.arrive)
	def OnArrive(self, data):
		entity, oldpos = data
		newpos = entity.sector
		# coming from out of view?
		if oldpos not in self.sectors:
			return self.OnNewEntity(entity)
		# otherwise
		self._UpdateViewState(newpos)
		return (perceptTypes.arrive, (id(entity), newpos))

	@signalhandler(signalTypes.entity_state_change)
	def OnEntityStateChange(self, data):
		entity, change = data
		self._UpdateViewState(entity.sector)
		return (perceptTypes.entity_state_change, (id(entity), change))

	@signalhandler(signalTypes.action)
	def OnAction(self, data):
		entity, action = data
		return (perceptTypes.action, (id(entity), action))

	@signalhandler(signalTypes.talk)
	def OnTalk(self, data):
		entity, message = data
		return (perceptTypes.talk, (id(entity), message))

	entity = property(lambda self: self._entityref())
	space = property(lambda self: self._spaceref())
