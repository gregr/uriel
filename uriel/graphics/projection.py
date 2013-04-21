# Gregory Rosenblatt
# 3/21/06

import renderer
import texture
from OpenGL.GL import *
from OpenGL.GLU import *


# immediate mode projections
class PerspectiveProjection:
	def __init__(self, rect, fovy=45, near=2.0, far=25.0):
		# what should the near/far values be?
		PushPerspectiveView(rect, fovy, near, far)
	def __del__(self):
		PopView()


class OrthogonalProjection:
	def __init__(self, rect, near=-1.0, far=1.0):
		PushOrthogonalView(rect, near, far)
	def __del__(self):
		PopView()


class SceneTextureSurface:	# re-render the scene when context invalidated
	def __init__(self, drawScene):
		self.drawScene = drawScene


def CopyToTexture(rect):
	x,y,w,h
	ww = texture.NextPowerOfTwo(w)
	hh = texture.NextPowerOfTwo(h)
	widthRatio = 1.0/ww
	heightRatio = 1.0/hh
	# create and bind tex id here
	glCopyTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA
					,x, renderer.CorrectedY(y,h), ww, hh, 0)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)


def PushPerspectiveProjection(rect, fovy, near, far):
	x,y,w,h = rect
	if h == 0:
		h = 1
	glViewport(x, renderer.CorrectedY(y,h), w, h)
	glMatrixMode(GL_PROJECTION)
	glPushMatrix()
	glLoadIdentity()
	gluPerspective(fovy, w/h, near, far)
#	glFrustum(-1.0, 1.0, -1.0, 1.0, near, far)
	glMatrixMode(GL_MODELVIEW)


def PushOrthogonalProjection(rect, near, far):
	x,y,w,h = rect
	if h == 0:
		h = 1
	y = renderer.CorrectedY(y,h)
	glViewport(x, y, w, h)
	glMatrixMode(GL_PROJECTION)
	glPushMatrix()
	glLoadIdentity()
	glOrtho(x, x+w, y+h, y, near, far)
	glMatrixMode(GL_MODELVIEW)


def PopProjection():
	w,h = renderer.screen.get_size()
	if h == 0:
		h = 1
	glViewport(0,0,w,h)
	glMatrixMode(GL_PROJECTION)
	glPopMatrix()
	glMatrixMode(GL_MODELVIEW)
