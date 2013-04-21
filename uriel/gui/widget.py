# Gregory Rosenblatt
# 3/9/06

import pygame
from weakref import ref, proxy

# add visibility and picking?
# picking is already handled by presence of OnGainFocus?
class Widget(object):
	#__slots__ = ["parent", "rect", "__weakref__"]
	def __init__(self, parent, pos=(0,0), size=(0,0)):
		if hasattr(parent, 'AddChild'):
			self._Attach(parent)
			x,y = pos
			self.rect = pygame.Rect((x + parent.rect.left
									,y + parent.rect.top), size)
		else:
			self.parent = None
			self.rect = pygame.Rect(pos, size)
	def _Attach(self, parent):
		parent.AddChild(self)
		self.parent = proxy(parent)
	def _Detach(self):	# some other name..?
		self.parent.children.remove(self)
		self.parent = None
	def Draw(self):
		self.OnDraw()
	def OnMove(self, dx, dy):
		self.rect.move_ip(dx, dy)
	def OnSize(self, size):
		self.rect.size = size
	def OnDraw(self):
		pass


def MoveWidgetToTop(w):
	active = set()
	p = w.parent
	if hasattr(w, "OnActivate"):
		active.add(ref(w, active.remove))
	while p:
		p.children.append(w)	# exception-safe order
		p.children.remove(w)
		w = p
		p = w.parent
		if hasattr(w, "OnActivate"):
			active.add(ref(w, active.remove))
	return active


def GetTopWidget(w):
	while hasattr(w, "children"):
		c = w.children
		if not c:
			break
		w = c[len(c)-1]
	return w
