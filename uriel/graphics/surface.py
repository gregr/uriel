# Gregory Rosenblatt
# 3/20/06

from uriel.core.resource import MakeResource
import pygame
from pygame.locals import *
from weakref import WeakValueDictionary


def Copy(target, source):
	ck = source.get_colorkey()
	if ck:
		source.set_colorkey()
		target.blit(source, (0,0))
		source.set_colorkey(ck, RLEACCEL)
		target.set_colorkey(ck, RLEACCEL)
	else:
		target.blit(source, (0,0))


def Save(surface, pathname):
	ck = surface.get_colorkey()
	surface.set_colorkey()
	pygame.image.save(surface, pathname)
	if ck:
		surface.set_colorkey(ck, RLEACCEL)


def _MakeSurface(pathname, colorKey):
	surface = pygame.image.load(pathname).convert()
	if colorKey:
		if colorKey is True:
			colorKey = surface.get_at((0,0))
		surface.set_colorkey(colorKey, RLEACCEL)
	return surface


pool = WeakValueDictionary()


def Surface(pathname, colorKey=None):
	return MakeResource((pathname, colorKey), _MakeSurface, pool)
