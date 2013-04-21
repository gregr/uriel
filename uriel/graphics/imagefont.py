# Gregory Rosenblatt
# 3/9/06

from texture import TextureSurface, UnbindTextures
from surface import Save
from font import Font
from uriel.core.resource import Resource
from OpenGL.GL import *
import pygame
import math
from weakref import WeakValueDictionary


defaultChars = "".join(chr(c) for c in xrange(1, 256))
defaultMargin = 2


def _CombineCharacters(surfaces, margin):
	width = sum(s.get_width()+margin for s in surfaces)
	height = max(s.get_height() for s in surfaces)
	target = pygame.Surface((width, height), pygame.SRCALPHA, 32)
	x = 0
	for s in surfaces:
		target.blit(s, (x, 0))
		x += s.get_width()+margin
	return target


def _CombineLines(surfaces):
	width = max(s.get_width() for s in surfaces)
	height = sum(s.get_height() for s in surfaces)
	target = pygame.Surface((width, height), pygame.SRCALPHA, 32)
	y = 0
	for s in surfaces:
		target.blit(s, (0, y))
		y += s.get_height()
	return target


def _CreateSurfaceAndMetrics(font, chars=defaultChars, margin=defaultMargin):
	charsPerRow = int(math.ceil(math.sqrt(len(chars))))
	length = len(chars)
	begin = 0
	rows = []
	while begin < length:
#		print "rendering:", chars[begin:end]
		row = [font.render(ch, True, (255,255,255))
				for ch in chars[begin:min(length, begin+charsPerRow)]]
		rows.append(_CombineCharacters(row, margin))
		begin += charsPerRow
	surface = _CombineLines(rows)
#	surface.set_colorkey((0,0,0))
	Save(surface, "checkfontsurface.bmp")
	surface = TextureSurface(surface)
	metrics = {}
	h = font.get_height()
	y = 0
	begin = 0
	while begin < length:
		end = min(length, begin+charsPerRow)
		x = 0
		for c in chars[begin:end]:
			w = font.size(c)[0]
			texcoords = (x*surface.widthRatio, y*surface.heightRatio
						,(x+w)*surface.widthRatio, (y+h)*surface.heightRatio)
			metrics[c] = (w, texcoords)
			x += w+margin
		y += h
		begin += charsPerRow
	return (surface, metrics)


class ImageFont(Resource):
	pool = WeakValueDictionary()
	def __construct__(self, font):
		self.surface, self.metrics = _CreateSurfaceAndMetrics(font)
		self.font = font
	def DrawString(self, s, pos):
		x,y = pos
		h = self.font.get_height()
		self.surface.Bind()	# how will color work?
		glBegin(GL_QUADS)
		for ch in s:
			w, tex = self.metrics[ch]
#			print "metrics:", w, tex
			u,v,uu,vv = tex
			glTexCoord2f(u, v)
			glVertex2i(x, y)
			glTexCoord2f(u, vv)
			glVertex2i(x, y+h)
			glTexCoord2f(uu, vv)
			glVertex2i(x+w, y+h)
			glTexCoord2f(uu, v)
			glVertex2i(x+w, y)
			x += w
		glEnd()
		UnbindTextures()


def LoadImageFont(name, size):
	return ImageFont(Font(name, size))
