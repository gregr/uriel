# Gregory Rosenblatt
# 3/31/06

#from uriel.core.struct
#from weakref import WeakValueDictionary

from pygame.locals import RESIZABLE

installed = None

def Install(name, **d):
	global installed
	assert not installed
	globals().update(d)
	installed = name
	Color.white = Color(1.0, 1.0, 1.0)	# maybe this should be done elsewhere?
	Color.black = Color(0.0, 0.0, 0.0)

#renderer = Struct()

#shader = surface or [texture, color=(white)]
#image = [shader, rect]

def Shader(surface, color=(1.0,1.0,1.0)):
	return surface

def EnableResizable():
	global videoFlags
	videoFlags |= RESIZABLE

def DisableResizable():
	global videoFlags
	videoFlags &= ~RESIZABLE

def Display(resolution, bgcolor=(0.0,0.0,0.0)):
	global fillColor
	fillColor = Color(*bgcolor)
	Resize(resolution)

def Resize(resolution):
	raise NotImplementedError

def Render(draw=lambda:None):
	raise NotImplementedError

def FillRect(rect):#color, rect):
	raise NotImplementedError

def Color(r, g, b, a=1.0):
	return (r,g,b,a)

def SetColor(color):
	raise NotImplementedError


def ScaleNormalToInteger(vals, scale=255):
	"""Create integer values from normalized values according to some scale."""
	return tuple(int(v*scale) for v in vals)


def ScaleIntegerToNormal(vals, scale=1.0/255.0):
	"""Create normalized values from integer values according to some scale."""
	return tuple(v*scale for v in vals)


#class TextLine:	# only one line of text
#	pool = WeakValueDictionary()	# store pygame text surfaces
#	def __init__(self, font, s=""):
#		self.str = s
#	def Draw(self, pos):
#		pass
