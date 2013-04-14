# Gregory Rosenblatt
# 3/12/06

from visibleentity import VisibleEntity
from settings import mediumTypes
from simulation.perception import *
from simulation.entity import *
from uriel.core.process import AddProcess
from uriel.core.weakmethod import MethodProxy

class Statue(VisibleEntity):
	def __init__(self, location, orient, **externalState):
		Entity.__init__(self, location, 'statue'
						,orient=orient, **externalState)

class SensorFloor(VisibleEntity):
	def __init__(self, location, sensingMedium, color, **externalState):
		Entity.__init__(self, location, 'floor'
						,color=color, **externalState)
		self.sensingMedium = sensingMedium
		space, sector = location
		sensorMap = space.signalHandlers[sensingMedium]
		self.sensor = Sensor(sensorMap, MethodProxy(self.OnSignal))
		self.sensor.ListenTo(GetRegionsInRange(space, sector
											,1, sensorMap.regionSize))
	def ChangeSector(self, sector):
		Entity.ChangeSector(self, sector)
		space = self.space()
		sensorMap = space.signalHandlers[self.sensingMedium]
		self.sensor.ListenTo(GetRegionsInRange(space, sector
											,1, sensorMap.regionSize))
	def OnSignal(self, signal):
		pass

class NameChangeFloor(SensorFloor):
	def __init__(self, location, **externalState):
		SensorFloor.__init__(self, location, mediumTypes.auditory, 11
							,**externalState)
	def OnSignal(self, signal):
		type, data, handled = signal
		if type == signalTypes.talk:
			entity, message = data
			if entity.sector == self.sector:
				if hasattr(entity, 'name'):
					if len(message) > 10:
						message = message[:10]
					def ChangeName():
						entity.name = message	# make process
						return
						yield None
					AddProcess(ChangeName())

class ClothingChangeFloor(SensorFloor):
	def __init__(self, location, clothing, **externalState):
		SensorFloor.__init__(self, location, mediumTypes.visual, clothing
							,**externalState)
		self._clothing = clothing
	def OnSignal(self, signal):
		type, data, handled = signal
		if type == signalTypes.arrive:
			entity, oldpos = data
			if entity.sector == self.sector:
				if hasattr(entity, 'clothing'):
					def ChangeClothing():
						entity.clothing = self._clothing	# make process
						return
						yield None
					AddProcess(ChangeClothing())
	def ChangeClothing(self, clothing):
		self._clothing = clothing
		self.ChangeExternalState(("color", clothing))

	clothing = property(lambda self: self._clothing, ChangeClothing)
