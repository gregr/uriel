# Gregory Rosenblatt
# 3/9/06

from widget import *


class Window(Widget):
	#__slots__ = ["children", __weakref__]
	def __init__(self, parent, pos=(0,0), size=(0,0)):
		Widget.__init__(self, parent, pos, size)
		self.children = []
	def AddChild(self, child):
		assert child not in self.children
		self.children.append(child)
	def Draw(self):
		self.OnDraw()
		# synchronize clipping with function scope
		clipper = self.clipper(self.rect)
		for child in self.children:
			child.Draw()
	def OnMove(self, dx, dy):
		self.rect.move_ip(dx, dy)
		for child in self.children:
			child.OnMove(dx, dy)
	def GetWidgetAtPos(self, pos):
		for child in reversed(self.children):
			if child.rect.collidepoint(*pos):
				if hasattr(child, "FindWidgetAtPos"):
					return child.FindWidgetAtPos(local)
				return child
		return self
