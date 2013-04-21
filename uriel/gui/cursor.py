# Gregory Rosenblatt
# 2/1/06

from uriel.core.tuplemath import Subtract2d
import pygame
from weakref import ref

class Cursor(object):
	#__slots__ = []
	def __init__(self, owner):
		self._ownerRef = ref(owner)
		self.local = owner
		self.mobileRegion = self.owner.rect
		self._pos = pygame.Rect((0,0), (0,0))	# tracks current and old pos
	def OnMove(self, rel):
		dx,dy = rel
		x,y = self.pos
		x += dx
		y += dy
		left, top = self.mobileRegion.topleft
		right, bottom = self.mobileRegion.bottomright
		if x < left:
			x = left
		elif x > right:
			x = right
		if y < top:
			y = top
		elif y > bottom:
			y = bottom
		pos = (x,y)
		self.pos = pos
		# send messages
		local = self.local
		if hasattr(local, "OnMouseMove"):
			local.OnMouseMove(self)
		next = self.owner.GetWidgetAtPos(pos)
		if next is not local:
			if hasattr(local, "OnMouseLeave"):
				local.OnMouseLeave(self)
			if hasattr(next, "OnMouseOver"):
				next.OnMouseOver(self)
			self.local = next
	def OnButtonUp(self, button):
		local = self.local
		if hasattr(local, "OnMouseButtonUp"):
			if not local.OnMouseButtonUp(self, button):	# keep cursor grab?
				self.mobileRegion = self.owner.rect
	def OnButtonDown(self, button):
		local = self.local
		self.owner.focus = local
		if hasattr(local, "OnMouseButtonDown"):
			grabber = local.OnMouseButtonDown(self, button)
			if grabber:
				self.mobileRegion = grabber.rect
	def _GetPos(self):
		return self._pos.topleft
	def _SetPos(self, pos):
		self._pos.size = self._pos.topleft
		self._pos.topleft = pos
	def _GetRel(self):
		return Subtract2d(self._pos.topleft, self._pos.size)
	def _GetOwner(self):
		return self._ownerRef()
	def _GetLocal(self):
		return self._localRef()
	def _SetLocal(self, local):
		self._localRef = ref(local)
	pos = property(_GetPos, _SetPos)
	rel = property(_GetRel)
	owner = property(_GetOwner)
	local = property(_GetLocal, _SetLocal)
