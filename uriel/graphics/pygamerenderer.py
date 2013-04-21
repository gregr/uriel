# Gregory Rosenblatt
# 3/20/06

from surface import Surface
import renderer
import pygame
from pygame.locals import *


def Install():

	class Clipper:
		def __init__(self, rect):
			screen = renderer.screen
			self.lastrect = screen.get_clip()
			screen.set_clip(rect)
		def __del__(self):
			renderer.screen.set_clip(self.lastrect)

	videoFlags = DOUBLEBUF

	def Resize(resolution):
		renderer.screen = pygame.display.set_mode(resolution
												,renderer.videoFlags)

	def Render(draw=lambda:None):
		renderer.screen.fill(renderer.fillColor)
		draw()
		pygame.display.flip()

	def FillRect(rect):
		renderer.screen.fill(renderer.color, rect)

	def Color(r, g, b, a=1.0):
		return renderer.ScaleNormalToInteger((r,g,b))

	def SetColor(color):
		renderer.color = color

	class Image(object):
		__slots__ = ["surf", "area"]
		def __init__(self, shader, area=None):
			self.surf = shader
			if area is None:
				area = shader.get_rect()
			self.area = area
		def Draw(self, pos):
			renderer.screen.blit(self.surf, pos, self.area)

	def LoadImage(pathname, colorKey=None, area=None):
		return Image(Surface(pathname, colorKey), area)

	renderer.Install(__name__, **locals())

Install()
