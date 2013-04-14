# Gregory Rosenblatt
# 3/18/06

import settings
from retardai import *
from perceiver import *
from testentities import *
from simulation.admincontroller import *
from simulation.adminplayercontroller import AdminPlayerController
from simulation.playercontroller import PlayerController
from simulation.sensor import SensorMap
from simulation.space import *
from simulation.agent import Agent, AgentUpdater
from uriel.net.userrealm import *
from uriel.core.process import Process, _mainGroup
#from uriel.core.timer import Timer
from twisted.internet import reactor
from twisted.cred import checkers

class VisualSpace(TerrainSpace):
	mediums = TerrainSpace.mediums + [settings.mediumTypes.visual]

def MakeWorld(size=(20,20,20)):
	signalHandlers = dict((medium, SensorMap(scale))
						for (medium, scale) in settings.mediumTraits)
	world = VisualSpace(signalHandlers, size)
	# make some terrain, for the love of god
	w,h,d = size
	gx = range(5,w-5)
	gy = range(5,h-5)
	for i in xrange(w):
		for j in xrange(h):
			if (i in gx) and (j in gy):
				world[(i,j,0)].terrain = 'grass'
			else:
				world[(i,j,0)].terrain = 'dirt'
	return world

world = MakeWorld()

def MakeClothingChangers(number=8, startSector=(5,0,1)):
	x,y,z = startSector
	clothingChangers = []
	for clothing in xrange(number):
		clothingChangers.append(ClothingChangeFloor((world, (x+clothing,y,z))
													,clothing))
	return clothingChangers

clothingChangers = MakeClothingChangers()

def MakeNameChangeStation(location):
	world, sector = location
	x,y,z = sector
	nameChanger = NameChangeFloor(location)
	leftStatue = Statue((world, (x-1,y,z)), 0)
	rightStatue = Statue((world, (x+1,y,z)), 1)
	return [nameChanger, leftStatue, rightStatue]

nameChangeStation = MakeNameChangeStation((world, (15,0,1)))

retard = Perceiver((world, (5,5,1)), "bob", 2)
retard.brain = HelloBrain(retard)

def DestroyCrap():
	global nameChangeStation
	for e in nameChangeStation:
		e.Destroy()
	del nameChangeStation
	global clothingChangers
	for c in clothingChangers:
		c.Destroy()
	del clothingChangers
	global retard
	retard.Destroy()
	del retard
#	global world
#	del world

def GenerateClothing(count=6):
	while True:
		for clothing in xrange(count):
			yield clothing


adminList = ["greg", "sal"]


class UserDatabase(UserRealm):
	"""Manages persistent user objects."""
	def __init__(self):
		UserRealm.__init__(self)
		self.controllers = {}
		self.clothing = GenerateClothing()
	def GetUser(self, avatarId, mind):
		"""Creates a user with an appropriate controller."""
		user = User(avatarId, mind)
		if avatarId == "admin":
			controller = AdminController(user.OnUpdate)
		else:
			perceiver = Perceiver((world, (1,1,1))
								,avatarId, self.clothing.next())
			perceiver.avatarId = avatarId	# track the id of player entities
			awareness = Awareness(user.OnUpdate)
			if avatarId in adminList:
				controller = AdminPlayerController(awareness, perceiver)
			else:
				controller = PlayerController(awareness, perceiver)
			controller.AddPerspective(retard.perception)	# for fun
#			awareness.Bind(retard.perception)	# for fun
		self.controllers[avatarId] = controller
		user.SetCommandHandler(controller.OnCommand)
		return user
	def ReleaseUser(self, avatarId):
		del self.controllers[avatarId]
		UserRealm.ReleaseUser(self, avatarId)


import pygame

running = True
clock = pygame.time.Clock()
MakeAdminConsole(locals())

agentUpdater = AgentUpdater()
processUpdater = Process.updater	#ProcessUpdater()

realm = UserDatabase()

def Stop():
	def KillSwitch():
		global running
		running = False
	reactor.callLater(5, KillSwitch)

def RunServer():
	checker = checkers.FilePasswordDB("userpasswords.txt")
	p = portal.Portal(realm, [checker])

	reactor.listenTCP(8123, pb.PBServerFactory(p))

	reactor.startRunning()
	try:
		while running:
			reactor.iterate()
			processUpdater.next()
			agentUpdater.next()
			clock.tick(settings.stepsPerSecond)
	except:
#		pass
		raise

def AssertCleanup():
	assert not Agent.pool
	assert not Perception.pool
	assert not Entity.pool
	assert not _mainGroup.processes
	assert not User.pool

RunServer()

DestroyCrap()

while _mainGroup.removedProcesses:
	print "cleaning processes"
	processUpdater.next()

print "processes remaining:", _mainGroup.processes

AssertCleanup()
