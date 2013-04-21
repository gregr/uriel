# Gregory Rosenblatt
# 1/23/06

from logutil import *
from twisted.spread import pb
from twisted.cred import portal, error
from twisted.python import failure
from weakref import WeakValueDictionary

class UserRealm:
	"""Produces and manages User objects when clients connect."""

	__implements__ = portal.IRealm

	def __init__(self):
		"""Prepare to handle connections."""
		self.users = {}

	def requestAvatar(self, avatarId, mind, *interfaces):
		"""Provide a new User when a client connects."""
		if pb.IPerspective not in interfaces: raise NotImplementedError
		if avatarId in self.users:
			return failure.Failure(error.DuplicateIdentity(avatarId))
		user = self.GetUser(avatarId, mind)
		self.users[avatarId] = user
		log.msg("%s logged in." % avatarId)
		return (pb.IPerspective, user, lambda: self.ReleaseUser(avatarId))

	def GetUser(self, avatarId, mind):
		"""Retrieve a User object based on a valid avatarId.
			
		Must be overriden.
		"""
		raise NotImplementedError

	def ReleaseUser(self, avatarId):
		"""Release a disconnected user.
			
		May be extended.
		"""
		assert avatarId in self.users
		self.users[avatarId].SetCommandHandler() # remove external attachments
		del self.users[avatarId]
		log.msg("%s disconnected." % avatarId)


class User(pb.Avatar):
	"""Represents a remote client."""

	pool = WeakValueDictionary()

	def __init__(self, avatarId, client, cmdHandler = lambda data:None):
		"""Establish an interface for communicating with a remote client."""
		User.pool[id(self)] = self
		self.client = client
		self.onCommand = cmdHandler

	def OnUpdate(self, data, guard=[]):
		"""Send an update to the client via RPC."""
		try:
			d = self.client.callRemote("Update", data)
			d.addCallback(LogAck)
			d.addErrback(LogErr)
		except pb.DeadReferenceError, e:
			if not guard:	# recursion guard
				guard.append(True)
				try:
					print e	# this could cause a recursing error
				finally:
					guard.pop()

	def SetCommandHandler(self, cmdHandler = lambda data:None):
		"""Set the callable used to handle incoming commands."""
		self.onCommand = cmdHandler

	def perspective_Command(self, data):
		"""Handle a command via RPC."""
#		try:
		return self.onCommand(data)
#		except Exception, e:	# alert the client of any error
#			raise pb.Error(e)
