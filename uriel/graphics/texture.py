# Gregory Rosenblatt
# 3/9/06

from surface import Surface, Copy as CopySurface
from uriel.core.resource import MakeResource, Resource
from OpenGL.GL import *
import pygame
import math
from weakref import WeakValueDictionary


def NextPowerOfTwo(n):
    return int(2.0 ** math.ceil(math.log(n)/math.log(2.0)))


def ExpandedSurface(surface):
	w,h = surface.get_size()
	expanded = pygame.Surface((NextPowerOfTwo(w), NextPowerOfTwo(h))
							,surface.get_flags(), surface)
	CopySurface(expanded, surface)
	return expanded


def UnbindTextures():
	glBindTexture(GL_TEXTURE_2D, 0)


class TextureId:
	def __init__(self):
		self.id = glGenTextures(1)
	def __del__(self):
#		if glIsTexture(self.id):	# this is useless
		glDeleteTextures(self.id)
#	def Bind(self):
#		glBindTexture(GL_TEXTURE_2D, self.id)

#TextureClass = Texture	# the class will still have the name 'Texture'


class TextureSurface(Resource):
	pool = WeakValueDictionary()
	def __construct__(self, surface):
		self.width, self.height = surface.get_size()
		self.surface = surface
		surface = ExpandedSurface(surface)
#		pygame.image.save(surface, "inspect%d.bmp" % id(self))
		w,h = surface.get_size()
		self.widthRatio, self.heightRatio = 1.0/w, 1.0/h
		data = pygame.image.tostring(surface, "RGBA", False)
		self.id = TextureId()
		self.Bind()
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA
					,surface.get_width(), surface.get_height()
					,0, GL_RGBA, GL_UNSIGNED_BYTE, data)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
	def Bind(self):
		glBindTexture(GL_TEXTURE_2D, self.id.id)


# this will also do the mipmapped textures
def Reload():	# necessary when opengl context is lost
	for s in TextureSurface.pool.itervalues():
		del s.id
	for args, s in TextureSurface.pool.iteritems():
		s.__construct__(*args)

#TextureSurfaceClass = TextureSurface


#def TextureSurface(surface):
#	return MakeResource((surface,), TextureSurfaceClass
#						,TextureSurfaceClass.pool)


def DrawTexturedRect(shader, rect, texCoords):
	x,y,w,h = rect
	u,v,uu,vv = texCoords
	glColor4f(1.0, 1.0, 1.0, 1.0)	# custom shader color later
	shader.Bind()
	glBegin(GL_QUADS)
	glTexCoord2f(u, v)
	glVertex2i(x, y)
	glTexCoord2f(u, vv)
	glVertex2i(x, y+h)
	glTexCoord2f(uu, vv)
	glVertex2i(x+w, y+h)
	glTexCoord2f(uu, v)
	glVertex2i(x+w, y)
	glEnd()
	UnbindTextures()


class Image(Resource):
	pool = WeakValueDictionary()
#	__slots__ = []
#	def __init__(self, surface, area=None):
	def __construct__(self, surface, area=None): # add color (shader?)
		self.surface = surface
		if area is None:
			area = (0,0,surface.width,surface.height)
		x,y,w,h = area
		xx, yy = x+w, y+h
		self.width, self.height = w, h
		self.area = (x*surface.widthRatio
						,y*surface.heightRatio
						,xx*surface.widthRatio
						,yy*surface.heightRatio)
	def Draw(self, pos):	# CW or CCW??
		DrawTexturedRect(self.surface, pos+(self.width, self.height)
						,self.area)
	def DrawStretched(self, rect):
		DrawTexturedRect(self.surface, rect, self.area)


def LoadImage(pathname, colorKey=None, area=None):
	return Image(TextureSurface(Surface(pathname, colorKey)), area)

#def Texture(surface, mipmapping=False):
#	return MakeResource((surface, mipmapping), MakeTextureImage, pool)


# this is actually a TextureSurface .... mipmaps will be actual textures
#def MakeTextureImage(surface):	# todo: mipmapping
#	surface = ExpandedSurface(surface)	# not necessary for mipmaps
#	data = pygame.image.tostring(surface, "RGBA", True)
#	tex = TextureClass()
#	glBindTexture(GL_TEXTURE_2D, tex.id)
#	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA
#				,surface.get_width(), surface.get_height()
#				,0, GL_RGBA, GL_UNSIGNED_BYTE, data)
#	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
#	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)


#pool = WeakValueDictionary()


#def Texture(surface, mipmapping=False):
#	return MakeResource((surface, mipmapping), MakeTextureImage, pool)

# example use
# newTexture = Texture(Surface(pathname, colorKey))
