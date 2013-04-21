# Gregory Rosenblatt
# 2/1/06

from uriel.common.percepts import *
from uriel.net.connection import *

class Controller:
	def __init__(self, model, onNewIdentity, onDelIdentity, onTalk
				,onAction=lambda p: None, onSound=lambda p: None
				,recordingFile=None):
		self.recordingFile = recordingFile
		self.eventHandlers = {
			perceptTypes.new_commands: self.OnNewCommands,
			perceptTypes.new_identity: onNewIdentity,
			perceptTypes.del_identity: onDelIdentity,
			perceptTypes.new_sector_group: model.OnNewSectorGroup,
			perceptTypes.new_sector: model.OnNewSector,
			perceptTypes.terrain_change: model.OnTerrainChange,
			perceptTypes.new_entity_group: model.OnNewEntityGroup,
			perceptTypes.new_entity: model.OnNewEntity,
			perceptTypes.del_entity: model.OnDelEntity,
			perceptTypes.depart: model.OnDepart,
			perceptTypes.arrive: model.OnArrive,
			perceptTypes.entity_state_change: model.OnEntityStateChange,
			perceptTypes.action: onAction,
			perceptTypes.sound: onSound,
			perceptTypes.talk: onTalk,
			perceptTypes.whisper: onTalk	# for now
			}
		self.actionMode = True
	def OpenConnection(self, configfile):
		connecting = [True]
		error = [False]
		def OnConnect():
			print "connection successful"
			connecting[0] = False
		def OnError():
			print "Error!"
			connecting[0] = False
			error[0] = True
		hostname = configfile.readline().strip()
		port = int(configfile.readline().strip())
		username = configfile.readline().strip()
		password = configfile.readline().strip()
		self.conn = Connection(hostname, port, username, password
								,self.OnUpdate, OnConnect, OnError)
		reactor.startRunning()
		while connecting[0]:
			reactor.iterate()
		if error[0]:
			raise SystemExit()
	def OnCommand(self, type, data):
		try:
			self.conn.OnCommand((type, data))
		except pb.DeadReferenceError, e:
			print e
	def OnUpdate(self, events):
		handlers = self.eventHandlers
		if self.recordingFile:
			for e in events:
				print >>self.recordingFile, e
		for e in events:
			type, data = e
			handlers[type](data)
	def OnNewCommands(self, names):
		self.commands = Enum(names)
