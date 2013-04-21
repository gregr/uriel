# Gregory Rosenblatt
# 4/12/06

from uriel.core.singleton import IsSingleton
import pygame
from pygame.locals import *
from weakref import proxy


#pygame's lifespan should match this module's
class _pygameGuard(object):
	"""Initializes and shuts down pygame with the lifespan of an instance."""

	def __init__(self):
		"""Initialize pygame."""
		assert IsSingleton(self)
		print "Initializing pygame..."
		pygame.init()

	def __del__(self):
		"""Shutdown pygame."""
		print "Shutting down pygame..."
		pygame.quit()

_guard = _pygameGuard()


class EventDispatcher(object):
	"""An event dispatcher for use with pygame.
		
	Dispatches pygame events to their appropriate handlers where specified.
	Only one instance should exist at any given time.
	"""

	def __init__(self, eventHandlers={}):
		"""Prepare the event loop.
			
		Only event types with handlers will be processed by the loop.
		If a handler for QUIT is not provided, a default will be used.
		"""
		assert IsSingleton(self)
		self.running = False
		self.ClearEventHandlers(eventHandlers)
		self.clock = pygame.time.Clock()

	def SetEventHandlers(self, eventHandlers):
		"""Set additional event handlers."""
		self.eventHandlers.update(eventHandlers)
		pygame.event.set_allowed(self.eventHandlers.keys())

	def ClearEventHandlers(self, newEventHandlers={}):
		"""Remove all event handlers and set any new handlers provided."""
		selfproxy = proxy(self)
		self.eventHandlers = {QUIT: lambda e: selfproxy.Stop()}
		pygame.event.set_allowed(None)
		self.SetEventHandlers(newEventHandlers)

	def Run(self, update=lambda:None, delay=0):
		"""Enter the pygame event loop.
			
		If provided, an update procedure will be called while looping.
		Each loop iteration will be delayed a given number of milliseconds.
		The loop is terminated by a call to Stop().
		"""
		try:
			self.running = True
			while True:
				for e in pygame.event.get():
					self.eventHandlers[e.type](e)
				update()
				pygame.time.wait(delay)
				self.clock.tick()
		except StopIteration:
			self.running = False
		except:
			self.running = False
			raise

	def Stop(self):
		"""Terminate a running event loop."""
		if self.running:
			raise StopIteration
