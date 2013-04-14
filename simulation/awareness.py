# Gregory Rosenblatt
# 3/5/06

from agent import Agent
from uriel.core.weakmethod import MethodProxy
from weakref import ref, WeakKeyDictionary


class Awareness(Agent):
	"""An Agent that draws input from perceptions within the simulation.
		
	All bound perceptions will transmit percepts for consumption by the mind
	program.
	"""

	def __init__(self, mind):
		"""Create an Awareness with 'mind' as the Agent program."""
		Agent.__init__(self, mind)
		self.spaces = {}	# spaces containing sectors viewed
		self.perspectives = WeakKeyDictionary()	# reference counted
		self._onSpaceDestroyed = MethodProxy(self.OnSpaceDestroyed)

	def GetViewState(self, space, sector):
		"""Determine the last viewed state of the given sector."""
		try:
			s = self.spaces[ref(space)]
		except KeyError:
			# send some percept for new space? and not when destroyed?
			self.spaces[ref(space, self._onSpaceDestroyed)] = {}
			return None
		if sector not in s:
			return None
		return s[sector]

	def SetViewState(self, space, sector, state):
		"""Remember the state of the sector being viewed."""
		try:
			s = self.spaces[ref(space)]
		except KeyError:	# currently, this should never happen
			# send some percept for new space? and not when destroyed?
			s = {}
			self.spaces[ref(space, self._onSpaceDestroyed)] = s
		s[sector] = state

	def OnSpaceDestroyed(self, spaceref):
		# send some percept for space deletion first?
		del self.spaces[spaceref]

	def AddPerspective(self, perception):
		if perception not in self.perspectives:
			self.Bind(perception)
			self.perspectives[perception] = 1
		else:
			self.perspectives[perception] += 1

	def RemovePerspective(self, perception):
		perspectives = self.perspectives
		perspectives[perception] -= 1
		if perspectives[perception] == 0:
			self.Unbind(perception)

	def Bind(self, perception):
		"""Register with a perception to receive percept transmissions."""
		perception.AttachAwareness(self)

	def Unbind(self, perception):
		"""Discontinue percept transmission from the given perception."""
		perception.DetachAwareness(self)
		try:
			del self.perspectives[perception]
		except KeyError:
			pass


class Perspective(object):
	""""""

	__slots__ = ["_aref", "_pref"]

	def __init__(self, awareness, perception):
		awareness.AddPerspective(perception)
		self._aref = ref(awareness)
		self._pref = ref(perception)

	def __del__(self):
		a = self.awareness
		if a:
			p = self._pref()
			if p:
				a.RemovePerspective(p)

	awareness = property(lambda self: self._aref())
