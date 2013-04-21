# Gregory Rosenblatt
# 4/9/06

from OpenGL.GL import *
from OpenGL.GLU import *


# later this becomes more complicated with moving cameras... matrixLookAt
# viewports?
def SetPerspectiveView(fovy, resolution, zrange):
	width, height = resolution
	if height == 0:
		height = 1
	near, far = range
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(fovy, float(width)/float(height), near, far)
	glMatrixMode(GL_MODELVIEW)


def SetOrthogonalView(quad, zrange):
	x,y,xx,yy = quad
	near, far = zrange
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(x, xx, y, yy, near, far)
	glMatrixMode(GL_MODELVIEW)


def SetRasterView(resolution, zdepth):
	width, height = resolution
	if height == 0:
		height = 1
	SetOrthogonalView((0.0,height,width,0.0), (0.0,zdepth))
