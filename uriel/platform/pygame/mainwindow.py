# Gregory Rosenblatt
# 4/9/06

from eventdispatcher import EventDispatcher
from uriel.gui.mainwindow import MainWindow as BaseMainWindow


class MouseHandler:
	def __init__(self, cursor):
		pygame.mouse.set_visible(False)
		self.cursor = cursor
		self.abspos = (0,0)
	def OnMove(self, event):
		self.abspos = event.pos
		self.cursor.OnMove(event.rel)
	def OnButtonUp(self, event):
		if pygame.event.get_grab():
			pygame.event.set_grab(False)
		self.cursor.OnButtonUp(event.button)
	def OnButtonDown(self, event):
		if not pygame.event.get_grab():
			pygame.event.set_grab(True)
			pygame.mouse.set_pos(self.cursor.pos)
			self.cursor.pos = self.abspos
		self.cursor.OnButtonDown(event.button)


class MainWindow(BaseMainWindow):
	def __init__(self):
		BaseMainWindow.__init__(self)
		self.mouseHandler = MouseHandler(self.cursor)
		def HandleDefault(event):
			print event
		selfproxy = proxy(self)
		self.SetEventHandlers({	# just pass as the dispatcher arguments?
					ACTIVEEVENT: HandleDefault,
					KEYDOWN: lambda e: selfproxy.focus.OnKeyDown(e),
					KEYUP: lambda e: selfproxy.focus.OnKeyUp(e),
					MOUSEMOTION: self.mouseHandler.OnMove,
					MOUSEBUTTONUP: self.mouseHandler.OnButtonUp,
					MOUSEBUTTONDOWN: self.mouseHandler.OnButtonDown,
					VIDEORESIZE: lambda e: selfproxy.OnSize(e.size)
					})
		self.dispatcher = EventDispatcher()
	def Run(self, onUpdate=lambda:None, delay=0):
		self.onUpdate = onUpdate
		EventDispatcher.Run(self, self.Update, delay)
	def _GetCaption(self):
		return pygame.display.get_caption[0]
	def _SetCaption(self, caption):
		pygame.display.set_caption(caption)
	caption = property(_GetCaption, _SetCaption)
