# Gregory Rosenblatt
# 4/9/06

# state key = (function, arguments)
# complete state = list of state keys
# geometry operation = vertex ops (opt. w/ tex coords) (opt. w/ color changes)
# complete operation = (complete state, geometry operation)
# map of complete ops = geom ops sorted by their complete state
# compiled = map processed into list of state change ops and geometry ops
# significant scene changes -> rebuild part/all of the map and compile

class RenderSequence:
	def __init__(self):
		self.map = {}
	def Append(self, ops):
		map = self.map
		for state, op in ops:
			try:
				map[state].append(op)
			except KeyError:
				map[state] = [op]
	def Compile(self, lastState):
		# often will need to create an empty state for the first 'lastState'
		seq = []
		for state, ops in sorted(self.map.iteritems()):
			seq += StateTransition(state, lastState) + ops
			lastState = state
		self.seq = seq
		self.map.clear()
		return lastState
	def __call__(self):
		for op in self.seq:
			op()


def StateTransition(state, lastState):
#	print "state, laststate:", len(state), len(lastState)
#	print state, lastState
	assert len(state) == len(lastState)
	lastState = iter(lastState)
	stateChangeOps = []
	for stateKey in state:
		if stateKey != lastState.next():
			stateChangeOps.append(StateChangeOperation(*stateKey))
	return stateChangeOps


def StateChangeOperation(func, *args):
	return lambda: func(*args)


emptyStateKey = (lambda: None,)


def Test():
	globalState = ['', '']	# image, underline

	def Image():
		return globalState[0]
	def Underline():
		return globalState[1]

	def DrawVertices(count):
		print
		print "drawing"
		for n in xrange(count):
			print Image(),
		print
		for n in xrange(count):
			print Underline(),
		print
		print

	def SetImage(img):
		globalState[0] = img
		print "image:", img
	
	def SetUnderline(ul):
		globalState[1] = ul
		print "underline:", ul

	firstState = (None, None)
	stateHashDash =((SetImage, '#'), (SetUnderline, '-'))
	stateAstDash = ((SetImage, '*'), (SetUnderline, '-'))
	stateHashCaret = ((SetImage, '#'), (SetUnderline, '^'))
	stateAstCaret = ((SetImage, '*'), (SetUnderline, '^'))
	ops = []
	ops.append((stateHashCaret, lambda: DrawVertices(10)))
	ops.append((stateAstDash, lambda: DrawVertices(5)))
	ops.append((stateAstCaret, lambda: DrawVertices(10)))
	ops.append((stateAstDash, lambda: DrawVertices(5)))
	ops.append((stateHashDash, lambda: DrawVertices(5)))
	ops.append((stateAstDash, lambda: DrawVertices(5)))
	ops.append((stateHashCaret, lambda: DrawVertices(10)))

	seq = RenderSequence()
	seq.Append(ops)
	seq.Compile(firstState)
	seq()
