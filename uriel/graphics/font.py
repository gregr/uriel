# Gregory Rosenblatt
# 3/9/06

from uriel.core.resource import MakeResource
import pygame
from weakref import WeakValueDictionary


pool = WeakValueDictionary()


def CreateFont(name, size):
	"""Load a TrueType Font using pygame.
		
	If the given name doesn't correspond to a valid font file, it will be
	used to load a system font.  If there is no such system font, the default
	font will be loaded instead.
	"""
	try:
		f = pygame.font.Font(name, size)
		return f
	except IOError:
		return pygame.font.SysFont(name, size)


def Font(name, size):
	return MakeResource((name, size), CreateFont, pool)
