# Gregory Rosenblatt
# 1/23/06

from logutil import *
from twisted.spread import pb
from twisted.internet import reactor
from twisted.cred import credentials

class Connection(pb.Referenceable):
	"""A connection supporting 2-way communication with a server.
		
	A reference to this controller is sent to the server when connecting.
	The server can send commands back through Remote Procedure Calls.
	"""

	def __init__(self, hostname, port, username, password, onUpdate
				,onConnect = lambda:None, onError = lambda:None):
		"""Connect to a server.
			
		Login is authenticated for the specified username and password.
		"""
		self.onConnect = onConnect
		self.onError = onError
		self.onUpdate = onUpdate
		factory = pb.PBClientFactory()
		reactor.connectTCP(hostname, port, factory)
		d = factory.login(credentials.UsernamePassword(username, password)
							,self)
		d.addCallback(self.OnConnect)
		d.addErrback(self.OnError)
	
	def __del__(self):
		"""Shutdown the connection."""
		self.Shutdown()

	def Shutdown(self):
		"""Stop the networking loop."""
		log.msg("Shutting down...")
		try:
			reactor.stop()
		except:
			log.err("Redundant shutdown attempted.")

	def OnConnect(self, perspective):
		"""Handle a connection event.
			
		This is passed to the 'Deferred' returned when initiating
		a connection with a server.
		"""
		self.perspective = perspective
		self.onConnect()

	def OnError(self, error):
		"""Shutdown and print an error message if a deferred call fails."""
		LogErr(error)
#		self.Shutdown()
		self.onError()

	def OnCommand(self, data, onResult=LogAck):
		"""Send a command via RPC."""
		d = self.perspective.callRemote("Command", data)
		d.addCallback(onResult)
		d.addErrback(self.OnError)

	def remote_Update(self, data):
		"""Handle an update via RPC."""
		# server doesn't need to know if this fails
		# the server should be infallable, so the problem is in the client
		try:
			return self.onUpdate(data)
		except Exception, e:	# the client might be out of date
			log.err("Unable to handle data: %s" % data)
			log.err(e)
