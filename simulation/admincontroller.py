# Gregory Rosenblatt
# 1/22/06

import code
import sys

console = None

def MakeAdminConsole(locals):
	global console
	console = code.InteractiveConsole(locals)

class OutputCatcher:
	def __init__(self, out):
		self.out = out
		self.listeners = set()
		self.buffer = ""
	def write(self, data):
		self.out.write(data)
		self.buffer += data
		if data[-1] == '\n':
			buf = self.buffer.rstrip()
			for l in self.listeners:
				l(buf)
			self.buffer = ""
	def flush(self):
		self.out.flush()

stdoutCatcher = OutputCatcher(sys.stdout)
stderrCatcher = OutputCatcher(sys.stderr)

sys.stdout = stdoutCatcher
sys.stderr = stderrCatcher

class AdminController:
	def __init__(self, listener):
		self.listener = listener
		stdoutCatcher.listeners.add(listener)
		stderrCatcher.listeners.add(listener)
	def __del__(self):
		stdoutCatcher.listeners.remove(self.listener)
		stderrCatcher.listeners.remove(self.listener)
	def OnCommand(self, data):
		assert console != None
		return console.push(data)
