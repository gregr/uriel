# Gregory Rosenblatt
# 4/1/06

import renderer
import imagefont
import texture
from OpenGL.GL import *
#from OpenGL.GLU import *
import pygame
from pygame.locals import *


def Install():

	class Clipper:
		current = None
		def __init__(self, rect):
			x,y,w,h = rect
			y = renderer.screen.get_height()-(y+h)
			if self.current is None:
				glEnable(GL_SCISSOR_TEST)
			self.lastrect = self.current
			glScissor(x,y,w,h)
			self.__class__.current = (x,y,w,h)
		def __del__(self):
			if self.lastrect is None:
				glDisable(GL_SCISSOR_TEST)
			else:
				glScissor(*self.lastrect)
			self.__class__.current = self.lastrect

	videoFlags = OPENGL|DOUBLEBUF

	def Resize(resolution, zdepth=10.0):
		renderer.screen = pygame.display.set_mode(resolution
												,renderer.videoFlags)
		SetViewport(resolution)

	def SetViewport(resolution):
		width,height = resolution
		if height == 0:
			height = 1
		glViewport(0, 0, width, height)
		SetProjection(resolution, zdepth)
		Initialize()

	def SetProjection(resolution, zdepth):
		width,height = resolution
		if height == 0:
			height = 1
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(0.0, width, height, 0.0, 0.0, zdepth)
		glMatrixMode(GL_MODELVIEW)

	def SetClearColor():
		glClearColor(*renderer.fillColor)
		glClearDepth(1.0)

	def SetDepthTest():	# a lot of this stuff will be meant for the GUI mode
		glEnable(GL_DEPTH_TEST)
		glDepthFunc(GL_LEQUAL)

	def Initialize():
		# a lot of this stuff won't actually be on by default
		glLoadIdentity()
		glEnable(GL_TEXTURE_2D)	##
		glShadeModel(GL_SMOOTH)	##
		SetClearColor()
		SetDepthTest()
		glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)	##
	#	glEnable(GL_ALPHA_TEST)
	#	glAlphaFunc(GL_GREATER, 0.0)
#		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) # transparency blend
		texture.Reload()

	def Render(draw=lambda:None):
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		draw()
		pygame.display.flip()

	def FillRect(rect):
		x,y,w,h = rect
		glRecti(x,y,x+w,y+h)
	
	def CorrectedY(y, h):
		return renderer.screen.get_height()-(y+h)

	SetColor = glColor4fv

	Image = texture.Image

	LoadImage = texture.LoadImage

	Font = imagefont.LoadImageFont

	renderer.Install(__name__, **locals())

Install()
