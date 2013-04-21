# Gregory Rosenblatt
# 2/28/06

from uriel.gui.eventdispatcher import EventDispatcher
from image import Image
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *


def Init():
	glEnable(GL_TEXTURE_2D)
	glShadeModel(GL_SMOOTH)
	glClearColor(0.0, 0.0, 0.0, 0.0)
	glClearDepth(1.0)
	glEnable(GL_DEPTH_TEST)
	glDepthFunc(GL_LEQUAL)
	glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
#	glEnable(GL_ALPHA_TEST)
#	glAlphaFunc(GL_GREATER, 0.0)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glEnable(GL_BLEND)


def Resize(size):
	width,height = size
	if height == 0:
		height = 1
	glViewport(0,0,width,height)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45, 1.0*width/height, 0.1, 100.0)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()


def Draw():
#	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	glTranslatef(0.0, 0.0, -4.0)
	glColor3f(1.0, 1.0, 1.0)
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(-1.0, -1.0, 0.0)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(1.0, -1.0, 0.0)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(1.0, 1.0, 0.0)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(-1.0, 1.0, 0.0)
	glEnd()
	glLoadIdentity()

# todo: non-'power of two' textures
# transparency from colorkeys
# sub-image through area rect
# mipmapping
def LoadTexture(pathname):
	img = Image(pathname, (255,0,0))
	img = img.img
	data = pygame.image.tostring(img, "RGBA", True)
	texid = glGenTextures(1)
	glBindTexture(GL_TEXTURE_2D, texid)
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA
				,img.get_width(), img.get_height()
				,0, GL_RGBA, GL_UNSIGNED_BYTE, data)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)


def TestTextureCopy(resolution):
	width, height = resolution
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	Draw()
	#pygame.display.flip()
	texid = glGenTextures(1)
	glBindTexture(GL_TEXTURE_2D, texid)
	glCopyTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 0, 0, width, height, 0)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

def DrawCopy():
	glTranslatef(0.0, 0.0, -4.0)
	glRotatef(30.0, 0.0, 0.0, 1.0)
	glColor3f(1.0, 1.0, 1.0)
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0)
	glVertex3f(-1.0, -1.0, 0.0)
	glTexCoord2f(1.0, 0.0)
	glVertex3f(1.0, -1.0, 0.0)
	glTexCoord2f(1.0, 1.0)
	glVertex3f(1.0, 1.0, 0.0)
	glTexCoord2f(0.0, 1.0)
	glVertex3f(-1.0, 1.0, 0.0)
	glEnd()
	glLoadIdentity()


class MainWindowGL(EventDispatcher):
	videoFlags = OPENGL|DOUBLEBUF|RESIZABLE
	def __init__(self, resolution):
		EventDispatcher.__init__(self)
		self.screen = pygame.display.set_mode(resolution, self.videoFlags)
	def Run(self, onUpdate=lambda:None):
		self.onUpdate = onUpdate
		EventDispatcher.Run(self, self.Update)
	def Update(self):
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		self.onUpdate()
		pygame.display.flip()
		pygame.time.wait(5)


size = (512, 512)
bgcolor = (0,64,64)
mw = MainWindowGL(size)#, bgcolor)
mw.caption = "test gui window"
Resize(size)
Init()
LoadTexture("glass.bmp")
TestTextureCopy(size)
print "max texture size:", GL_MAX_TEXTURE_SIZE
mw.Run(DrawCopy)
