# Gregory Rosenblatt
# 3/18/06

import pygame
from pygame.locals import *
from collections import deque
import os

# eventually, most (all?) of these will be refactored into the gui (i think)

class InputText:
	def __init__(self, font):
		self.font = font
		self.Clear()
	def AddChar(self, ch):
		self.value += ch
#		self.Refresh()
	def DelChar(self):
		l = len(self.value)
		if l > 0:
			self.value = self.value[:len(self.value)-1]
#			self.Refresh()
	def Clear(self):
		self.value = ""
#		self.Refresh()
#	def Refresh(self):
#		self.text = self.font.render(self.value, 1, (255,255,255))

class MessageHistory:
	def __init__(self, font):
		self.font = font
		self.lines = deque()
	def Add(self, msg):
		self.lines.append(msg)#self.font.render(msg, 1, (0,191,255)))
		while len(self.lines) > 6:
			self.lines.popleft()

def LoadImage(name, colorKey=None):
	fullname = os.path.join('data', name)
	try:
		image = pygame.image.load(fullname)
	except pygame.error, msg:
		print 'Cannot load:', fullname
		raise SystemExit, msg
	image = image.convert()
	if colorKey is not None:
		if colorKey is -1:
			colorKey = image.get_at((0,0))
		image.set_colorkey(colorKey, RLEACCEL)
	return image
