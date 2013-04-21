# Gregory Rosenblatt
# 3/21/06

import renderer, openglrenderer
from uriel.gui.eventdispatcher import EventDispatcher
from OpenGL.GL import *


resolution = (400, 400)
bgcolor = (0.25, 0.5, 0.75, 0.0)
red = renderer.Color(0.75, 0.0, 0.0, 0.5)
green = renderer.Color(0.0, 0.5, 0.0, 0.3)
textColor = renderer.Color(0.5,0.0,0.8)

dispatcher = EventDispatcher()
renderer.Display(resolution, bgcolor)

font = renderer.Font(None, 16)
img = renderer.LoadImage("glass.bmp", (255,0,0), (0,0,80,80))
def Draw(counter=[0]):
	renderer.SetColor(red)
	renderer.FillRect((50, 70, 100, 75))
	renderer.SetColor(green)
	renderer.FillRect((100, 70, 100, 75))
	renderer.FillRect((100, 170, 100, 75))
	renderer.SetColor(red)
	renderer.FillRect((50, 170, 100, 75))
	#renderer.FillRect((10,389,60,1))
	renderer.SetColor(textColor)
	#glColor3fv((0.5,0.0,0.8))
	font.DrawString("abcd ABCD 12345 ! @ # $", (30, 40))
	img.Draw((280, 60))
	if counter[0] > 200:
		print dispatcher.clock
		counter[0] = -1
	counter[0] += 1

dispatcher.Run(lambda: renderer.Render(Draw))
