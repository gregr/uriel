# Gregory Rosenblatt
# 4/12/06

from uriel.graphics import renderer
from cursor import Cursor
from window import *
from uriel.core.weakmethod import MethodProxy
from weakref import ref, proxy


# mainwindow brush will contain bg color and cursor data
class MainWindow(Window):
	def __init__(self, resolution, bgcolor=(0.0,0.0,0.0,0.0), resizable=True):
		EventDispatcher.__init__(self)
		Window.__init__(self, None, (0, 0), resolution)
		self._active = set()
		self._focusRef = ref(self)
		self.cursor = Cursor(self)

		if not renderer.installed:	# later, insist that it be installed first?
			import uriel.graphics.pygamerenderer
		if resizable:
			renderer.EnableResizable()
		renderer.Display(resolution, bgcolor)
		Window.clipper = renderer.Clipper
		print renderer.installed
		white = renderer.Color(1.0,1.0,1.0)
		self.SetDefaultCursorDrawFunc(
				lambda pos: renderer.FillRect(white, pygame.Rect(pos, (1,1))))
	def SetDefaultCursorDrawFunc(self, draw):	# what an ugly method name
		self.DefaultDrawCursor = draw
		self.DrawCursor = draw
	def Draw(self):
		Window.Draw(self)
		self.DrawCursor(self.cursor.pos)
	def OnSize(self, size):
		Window.OnSize(self, size)
		renderer.Resize(size)
	def OnKeyDown(self, data):
		print data
	def OnKeyUp(self, data):
		print data
	def MakeUpdater(self, task=lambda:None):
		def Update():
			task()
			renderer.Render(self.Draw)
		return Update
	def _GetFocus(self):
		return self._focusRef()
	def _SetFocus(self, widget):
		focus = self.focus
		active = MoveWidgetToTop(widget)
		deactivate = self._active - active
		activate = active - self._active
		self._active = active
		for w in deactivate:
			w.OnDeactivate()
		for w in activate:
			w.OnActivate()
		while widget:
			if hasattr(widget, "OnGainFocus"):
				if widget is not focus:
					if hasattr(focus, "OnLoseFocus"):
						focus.OnLoseFocus()
				self._focusRef = ref(widget, MethodProxy(self._ResetFocus))
				widget.OnGainFocus(self)
				return
			widget = widget.parent
		if not focus:
			self._focusRef = ref(self)
	def _ResetFocus(self, r):
		if r() is not self:
			self.focus = GetTopWidget(self)
	focus = property(_GetFocus, _SetFocus)
