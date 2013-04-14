# Gregory Rosenblatt
# 3/23/06

from uriel.core.enum import *
from uriel.core.tuplemath import IntegerScale3d as ScaleSector
from weakref import proxy, ref

# todo:
# obscurers and filters
# eventually make a distinction between actual signal type and medium
# ie. detection, communication vs. visual, auditory, radio, esp, etc. maybe...

# a signal handler must not directly generate new signals
# new signals should be deferred through an Agent
def _DispatchSignal(signal, sensors, dispatching=[]):
	assert not dispatching
	dispatching.append(True)
	for s in sensors:
		s.onSignal(signal)
	dispatching.pop()


class SensorMap:
	"""Spatial mapping of sensors that listen for a given signal type."""

	def __init__(self, regionSize = 1):
		"""Create a map that binds sensors to regions of the given size.
			
		Each region is a cube containing regionSize^3 sectors.
		"""
		self.mapped = {}
		self.regionSize = regionSize

	def AddSensor(self, sensor, regions):
		"""Register the sensor to the given regions."""
		mapped = self.mapped
		for r in regions:
			if r not in self.mapped:
				mapped[r] = set()
			mapped[r].add(ref(sensor, mapped[r].remove))

	def RemoveSensor(self, sensor, regions):
		"""Remove the sensor from the given regions."""
		mapped = self.mapped
		for r in regions:
			mapped[r].discard(ref(sensor))
			if len(mapped[r]) == 0:
				del mapped[r]

	def OnSignal(self, signal, sectors):
		"""Send a signal to sensors listening to any of the given sectors."""
		mapped = self.mapped
		factor = 1.0/self.regionSize
		transform = lambda s: ScaleSector(s, factor)
		regions = set(map(transform, sectors))
		signaled = set()
		for r in regions:
			if r in mapped:
				for s in mapped[r]:
					signaled.add(s())
		_DispatchSignal(signal, signaled)
#		for s in signaled:
#			s.onSignal(signal)


def DefaultHandler(data):
	print "Signal Detected:", data


class Sensor:
	"""A listener that receives signals of a particular type.
		
	The signal type listened for is determined by the map to which the sensor
	is registered.  Sensors register themselves with a set of regions to listen
	to for signals.
	"""

	def __init__(self, map, handler=DefaultHandler):
		"""Create a sensor that calls the given handler when signaled.
			
		Storage of the given handler must not cause circular referencing.
		"""
		self.regions = set()
		self.map = proxy(map)
		self.onSignal = handler

	def __del__(self):
		"""Removes the sensor from the map it was registered to."""
		try:
			self.map.RemoveSensor(self, self.regions)
		except ReferenceError:
			pass	# during top-down destruction, this might be raised

	def ChangeMap(self, map):
		"""Register the sensor with a different map."""
		self.map.RemoveSensor(self, self.regions)
		self.regions.clear()
		self.map = proxy(map)

	def ListenTo(self, regions):
		"""Listen only to the given regions."""
		scrapped = self.regions - regions
		added = regions - self.regions
		self._RemoveRegions(scrapped)
		self._AddRegions(added)

	def _AddRegions(self, regions):
		"""Listen to additional regions."""
		self.regions |= regions
		self.map.AddSensor(self, regions)

	def _RemoveRegions(self, regions):
		"""Stop listening to the given regions."""
		self.map.RemoveSensor(self, regions)
		self.regions -= regions
