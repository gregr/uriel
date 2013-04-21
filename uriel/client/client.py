# Gregory Rosenblatt
# 3/19/06

from view import *
from model import *
from controller import *
from uriel.gui.mainwindow import *
#from uriel.gui.image import Image
from uriel.graphics import renderer, openglrenderer
from twisted.internet import reactor
import code
import sys
import os.path

Image = renderer.LoadImage

Font = renderer.Font

identities = set()

model = Model()

mw = MainWindow((400,500), (0.0625,0.125,0.25))	# nice ugly gray-blue
mw.caption = "Client View"
cursorPathName = os.path.join("data", "cursors.bmp")
cursorImage = Image(cursorPathName, True, (13,0,12,17))
mw.SetDefaultCursorDrawFunc(cursorImage.Draw)

actionModeString = "[ Action Mode ]"
textModeString = "[ Text Mode ]"
interpreterModeString = "[ Interpreter Mode ]"

font = Font(None, 20)
lineHeight = font.font.get_linesize()
inputBoxHeight = (pygame.display.get_surface().get_height()
					-(lineHeight+lineHeight))

view = View(mw, font, model, (10, 100))
inputBox = InputBox(mw, font, actionModeString, (0, inputBoxHeight))
messageBox = MessageBox(mw, font)

# pygame.font.render is too much of a wuss... we'll have to wait
#class OutputCatcher:
#	def __init__(self, out):
#		self.out = out
#		self.buffer = ''
#	def write(self, s):
#		self.out.write(s)
#		self.buffer += s
#		if s[-1] == '\n':
#			messageBox.history.Add(self.buffer.rstrip())
#			self.buffer = ''

#sys.stdout = OutputCatcher(sys.stdout)
#sys.stderr = OutputCatcher(sys.stderr)

def TogglePerspective():
	if not view.identity:
		return
	identList = list(identities)
	identList.sort()
	i = identList.index(view.identity)+1
	if i >= len(identList):
		i = 0
	view.identity = identList[i]
	print "perspective toggled"

def OnNewIdentity(ident):
	identities.add(ident)
	if not view.identity:
		view.identity = ident

def OnDelIdentity(ident):
	identities.remove(ident)
	if ident == view.identity:
		if not identities:
			view.identity = None
		else:
			view.identity = identities.pop()	# annoying sets...
			identities.add(view.identity)

def OnTalk(data):
	ident, message = data
	speaker = 'Unknown voice'
	entities = model.entities
	if ident in entities:
		speaker = entities[ident].name
	msg = '%s says: %s' % (speaker, message)
	messageBox.history.Add(msg)

possessed = None

def OrientPossessed(direction):
	controller.OnCommand(controller.commands.command_entity
						,(possessed, controller.commands.orient, (direction,)))
def MovePossessed(direction):
	controller.OnCommand(controller.commands.command_entity
						,(possessed, controller.commands.move, (direction,)))

def MakeActionKeyHandlers(controller):
	def TogglePossess():
		global possessed
		if not possessed:
			ent = model.entities[view.identity]
			for e in model.spaces[ent.space][ent.sector].entities:
				if e is not view.identity:
					possessed = e
					controller.OnCommand(controller.commands.take_control
										,(possessed,))
					return
		else:
			controller.OnCommand(controller.commands.restore_control
								,(possessed,))
			possessed = None
	def Test():
		controller.OnCommand(controller.commands.test, ('hooray beer',))
	def Orient(direction):
		controller.OnCommand(controller.commands.orient, (direction,))
	def Move(direction):
		controller.OnCommand(controller.commands.move, (direction,))
	def TextMode():
		controller.actionMode = False
		inputBox.SetModeText(textModeString)
	def InterpreterMode():
		controller.actionMode = None
		inputBox.SetModeText(interpreterModeString)
	def MoveUp():
		Orient(0)
		Move(0)
	def MoveRight():
		Orient(1)
		Move(1)
	def MoveDown():
		Orient(2)
		Move(2)
	def MoveLeft():
		Orient(3)
		Move(3)
	def SaveScreenshot():
#		pygame.image.save(pygame.display.get_surface(), "screenshot.bmp")
		print "saved screenshot.bmp", "currently broken"
	keyHandlers = {	(KMOD_NONE, K_1): Test,
					(KMOD_NONE, K_F12): SaveScreenshot,
					(KMOD_NONE, K_RETURN): TextMode,
					(KMOD_NONE, K_TAB): InterpreterMode,
					(KMOD_NONE, K_HOME): TogglePerspective,
					(KMOD_NONE, K_END): TogglePossess,
					(KMOD_NONE, K_UP): MoveUp,
					(KMOD_NONE, K_RIGHT): MoveRight,
					(KMOD_NONE, K_DOWN): MoveDown,
					(KMOD_NONE, K_LEFT): MoveLeft,
					(KMOD_LSHIFT, K_UP): lambda: Orient(0),
					(KMOD_LSHIFT, K_RIGHT): lambda: Orient(1),
					(KMOD_LSHIFT, K_DOWN): lambda: Orient(2),
					(KMOD_LSHIFT, K_LEFT): lambda: Orient(3)
					}
	return keyHandlers

def MakeTextKeyHandlers(controller):
	def Talk():
		inputtext = inputBox.inputtext
		if len(inputtext.value) > 0:
			controller.OnCommand(controller.commands.talk, (inputtext.value,))
			inputtext.Clear()
		controller.actionMode = True
		inputBox.SetModeText(actionModeString)
	keyHandlers = {
		(KMOD_NONE, K_RETURN): Talk,
		(KMOD_NONE, K_BACKSPACE): lambda: inputBox.inputtext.DelChar()
		}
	return keyHandlers

console = code.InteractiveConsole(locals())

def MakeInterpreterKeyHandlers(controller):
	def Eval(more=[False]):
		inputtext = inputBox.inputtext
		if (len(inputtext.value) > 0) or more[0]:
			more[0] = console.push(inputtext.value)
			inputtext.Clear()
			if more[0]:
				return
		controller.actionMode = True
		inputBox.SetModeText(actionModeString)
	keyHandlers = {
		(KMOD_NONE, K_RETURN): Eval,
		(KMOD_NONE, K_BACKSPACE): lambda: inputBox.inputtext.DelChar()
		}
	return keyHandlers

recordingFile = open('lastrecording.txt', 'w')
controller = Controller(model, OnNewIdentity, OnDelIdentity, OnTalk
						,recordingFile)
controller.OpenConnection(open('clientconfig.txt'))

actionHandlers = MakeActionKeyHandlers(controller)
textHandlers = MakeTextKeyHandlers(controller)
interpreterHandlers = MakeInterpreterKeyHandlers(controller)

def OnKeyDown(k):
	id = (k.mod, k.key)
	try:
		if controller.actionMode:
			if id in actionHandlers:
				actionHandlers[id]()
#			elif k.unicode:	# this doesn't exist anymore
#				controller.OnCommand(controller.commands.action, (k.unicode,))
		elif controller.actionMode is False:
			if id in textHandlers:
				textHandlers[id]()
			elif k.unicode:
				inputBox.inputtext.AddChar(k.unicode)
		else:
			if id in interpreterHandlers:
				interpreterHandlers[id]()
#			if k.key == K_TAB:
#				print "unicode:", ord(k.unicode)
			elif k.unicode:
				inputBox.inputtext.AddChar(k.unicode)
	except AttributeError, e:
		print "Command error:", e

mw.OnKeyDown = OnKeyDown
mw.OnKeyUp = lambda _: None
#mw.SetEventHandlers({KEYDOWN: OnKeyDown})
mw.Run(reactor.iterate)
