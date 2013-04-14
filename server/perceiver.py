# Gregory Rosenblatt
# 3/10/06

from visibleentity import VisibleEntity
from settings import mediumTypes
import settings
from simulation.perception import *
from simulation.entity import *
from simulation.entitycontroller import EntityController
from uriel.core.weakmethod import MethodProxy
from uriel.core.functionmap import MakeFunctionMap
from uriel.core.tuplemath import Add3d as SectorAdd


perceiverSenses = {mediumTypes.visual: settings.visualRange
					,mediumTypes.auditory: settings.auditoryRange}


class Perceiver(VisibleEntity):
	# say, tell, move, turn, use, update, show, whatever ...
	actionTypes = Enum(["talk", "move", "orient"])
	moveDeltas = [(0,-1,0), (1,0,0), (0,1,0), (-1,0,0)]
	def __init__(self, location, name, clothing, **externalState):
		Entity.__init__(self, location, 'perceiver'
						,name=name, clothing=clothing, orient=0
						,**externalState)
		self.moveDelay = 10
		self.perception = Perception(self, perceiverSenses
									,[mediumTypes.visual])
		self.controller = EntityController(self)
#	def Destroy(self):
#		self.controller.Destroy()
#		self.perception.Destroy()
#		Entity.Destroy(self)
	def ChangeSector(self, sector):
		Entity.ChangeSector(self, sector)
		self.perception.ChangeSector(sector)
	def ChangeSpace(self, location):
		Entity.ChangeSpace(self, location)
		self.perception.ChangeSpace(location)
	def ChangeName(self, name):
		self.ChangeExternalState(('name', name))
	def ChangeClothing(self, clothing):
		self.ChangeExternalState(('clothing', clothing))
	def Move(self, direction):
		try:
			sector = SectorAdd(self.sector, self.moveDeltas[direction])
			s = self.space[sector]	# see if the sector index is valid
			self.ChangeSector(sector)
			self.controller.StartCoolOff("move")
		except KeyError:
			pass

#	def MoveCoolOffUpdater(self, callback=lambda:None):
#		self = proxy(self)
#		while self.moveCoolOff < self.moveDelay:
#			self.moveCoolOff += 1
#			print "updating: moveCoolOff", self.moveCoolOff
#			yield None
#		del self.moveCoolOff
#		callback()

	def OnCommand(self, data):
		self.controller.OnAction(*data)

	actions, actionhandler = MakeFunctionMap()

	def OnAction(self, type, args):
#		if type in self.actions:
		self.actions[type](self, *args)

	@actionhandler(actionTypes.talk)
	def OnTalk(self, message):
		self.space.OnSignal(TalkSignal([mediumTypes.auditory]
										,self, message))

	@actionhandler(actionTypes.move)
	def OnMove(self, direction):
		self.controller.CallAfterCoolOff("move"
										,MethodProxy(self.Move, direction))

	@actionhandler(actionTypes.orient)
	def OnOrient(self, orient):
		if orient == self.orient:
			return
		if orient < 0:
			orient = 0
		elif orient >= 4:
			orient = 3
		self.ChangeExternalState(('orient', orient))

	name = property(lambda self: self.externalState.name
					,ChangeName)
	clothing = property(lambda self: self.externalState.clothing
						,ChangeClothing)
	orient = property(lambda self: self.externalState.orient
						,OnOrient)
