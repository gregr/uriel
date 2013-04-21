# Gregory Rosenblatt
# 3/20/06

from mainwindow import MainWindow
from window import Window
#from widget import Widget
from uriel.graphics import renderer, openglrenderer
from OpenGL.GL import *


class ColoredWindow(Window):
	def __init__(self, parent, pos, size, color):
		Window.__init__(self, parent, pos, size)
		self.color = renderer.Color(*color)
	def OnDraw(self):
		glColor4f(*self.color)
		renderer.FillRect(self.rect)
#		Window.OnDraw(self)


class FlyingText(ColoredWindow):
	def __init__(self, parent, pos, size, color, font, textcolor, text=""):
		ColoredWindow.__init__(self, parent, pos, size, color)
		self.font = font
		self.textcolor = renderer.Color(*textcolor)
		self.text = text
	def OnDraw(self):
		ColoredWindow.OnDraw(self)
		glColor4f(*self.textcolor)
		self.font.DrawString(self.text, self.rect.topleft)
		glColor3f(1.0,1.0,1.0)


mw = MainWindow((400,400), (0.0,0.25,0.25,0.0))
mw.caption = "test gui window"

# todo: make cursor image with hotspot
Image = renderer.LoadImage
cursorImage = Image("cursors.bmp", True, (1,0,12,17))
mw.SetDefaultCursorDrawFunc(cursorImage.Draw)

for i in xrange(10):
	pos = (i*10,i*10)
	size = (20,20)
	color = (0, i*0.05, i*0.1)
	ColoredWindow(mw, pos, size, color)
cw = ColoredWindow(mw, (150,150), (80,80), (1.0,1.0,1.0))
ColoredWindow(cw, (10, 10), (20, 20), (0.0,0.0,0.0))

FlyingText(mw, (50, 50), (100, 30), (0.25,0.5,0.0,0.5)
		,renderer.Font("arialms", 20), (1.0,1.0,1.0)
		,"~ ! @ # $ % ^ & * ( ) i hope this works...")

clockText = FlyingText(mw, (20, 300), (80, 20), (0.0, 0.0, 0.0)
					,renderer.Font(None, 16), (1.0,1.0,1.0)
					,"FPS: N/A")

def UpdateClock(counter=[0]):
	if counter[0] > 200:
		clockText.text = "FPS: %d" % mw.clock.get_fps()
		counter[0] = -1
	counter[0] += 1

mw.Run(UpdateClock, 5)
