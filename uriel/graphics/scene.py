# Gregory Rosenblatt
# 3/31/06

from weakref import proxy


class Brush:	# set as opaque or transparent (with alpha value)
	renderer = None
	def __init__(self, alpha=1.0):
		self.alpha = alpha
		self.ops = []
	def Draw(self):
		self.renderer.AddOperations(self.ops, self.alpha)


# texture=None indicates unbinding textures
# color=None indicates an operation that will specify its own colors
def RenderState(texture=None, clipRect=None, color=None, mode=None):
	return [texture, clipRect, color, mode]

def MakeOpaqueState(state, zorder):
	mode = state[len(state)-1]
	return state[:len(state)-1]+[zorder, mode]

def MakeTransparentState(state, zorder, alpha):
	state = [zorder]+state
	state.append(alpha)	# this alpha/color order might not be right
	return state

def GetMode(state):
	return state[len(state)-1]

def ExecuteOperations(mode, ops):
	glBegin(mode)
	for op in ops:
		op()
	glEnd()

class RenderPass:
	def __init__(self):
		self.queue = {}
	def AddOperations(self, ops, formatState, *args):	# extra state args
		for state, op in ops:
			state = formatState(state, *args)
			try:
				self.queue[state].append(op)
			except KeyError:
				self.queue[state] = [op]
	def Draw(self, oldState, stateTransition):
		queue = self.queue
		for state in sorted(queue.iterkeys()):
			stateTransition(state, oldState)
			print "state change:", state
			mode = GetMode(state)
			ExecuteOperations(mode, queue[state])
		return state

class OpaquePass(RenderPass):
	def AddOperations(self, ops, zorder):
		RenderPass.AddOperations(self, ops, MakeOpaqueState, zorder)
	def Draw(self, oldState):
		return RenderPass.Draw(self, oldState, ChangeOpaqueState)

class TransparentPass(RenderPass):
	def AddOperations(self, ops, zorder, alpha):
		RenderPass.AddOperations(self, ops, MakeTransparentState
								,zorder, alpha)
	def Draw(self, oldState):
		EnableBlending()
		state = RenderPass.Draw(self, oldState, ChangeTransparentState)
		DisableBlending()
		return state


def EnableBlending():
	glEnable(GL_BLEND)
#	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)	# only done once...?
	glDepthMask(GL_FALSE)

def DisableBlending():
	glDepthMask(GL_TRUE)
	glDisable(GL_BLEND)

# RenderingManager? InterfaceRenderer? Ortho2DScene?
# provides an interface to gather opaque or transparent operations
# Opaque or Transparent RenderOperation(state, vertexOp)

class InterfaceSceneRenderer:
	def __init__(self, root):
		self.root = proxy(root)
		self.valid = False
		self.opaquePass = OpaquePass()
		self.transparentPass = TransparentPass()
		self.state = RenderState()
	def AddOperations(self, ops, alpha):
		if alpha != 1.0:
			self.transparentPass.AddOperations(ops, self.zorder, alpha)
		else:
			self.opaquePass.AddOperations(ops, self.zorder)
		self.zorder += 0.1
	def Draw(self):
		if not self.valid:
			self.zorder = 0.0
			self.opaquePass.queue.clear()
			self.transparentPass.queue.clear()
			self.root.Draw()
			# set proper projection z-buffer depth according to self.zorder
			self.valid = True
		state = self.opaquePass.Draw(self.state)
		# state needs to be formatted to transparent first
		self.state = self.transparentPass.Draw(state)


def ChangeOpaqueState(newState, oldState):
	pairs = zip(ReorderState(newState), ReorderState(oldState))
	texture, clipRect, color, zorder, mode = pairs
	a,b = texture
	if a != b:
		SetTextureState(a)
	a,b = clipRect
	if a != b:
		SetClippingState(a)
	a,b = color
	if a != b:
		SetColorState(a)
	a,b = zOrder
	if a != b:
		SetZOrderState(a)

_globalAlpha = 1.0

def ChangeTransparentState(newState, oldState):
	pass

def SetTextureState(texture):
	texture.Bind()

def SetClippingState(clipRect):
	pass

def SetZOrderState(zorder):
	glTranslatef(0.0, 0.0, zorder)

def SetColorState(color):
	glColor4fv(color)

def SetAlphaColorState(color):
	r,g,b,a = color
	glColor4f(r,g,b,a*_globalAlpha)
