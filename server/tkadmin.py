# Gregory Rosenblatt
# 3/5/06

from uriel.net.connection import Connection
from twisted.internet import reactor, tksupport
from Tkinter import *
from ScrolledText import ScrolledText


class Terminal(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.pack()
		self.CreateWidgets()
		self.prompt = '>>> '
		configfile = open('adminclientconfig.txt', 'r')
		hostname = configfile.readline().strip()
		port = int(configfile.readline().strip())
		username = configfile.readline().strip()
		password = configfile.readline().strip()
		self.conn = Connection(hostname, port, username, password
						,self.ReceiveMessage
						,lambda: self.ReceiveMessage("connection successful")
						,lambda: self.ReceiveMessage("ERROR!!!!"))
	def destroy(self):
		self.conn.Shutdown()
		Frame.destroy(self)
	def CreateWidgets(self):
		self.text = ScrolledText(self, state=DISABLED, height=30)
		self.text["fg"] = "white"
		self.text["bg"] = "black"
		self.text.pack()
		self.entry = Entry(self)
		self.entry["fg"] = "white"
		self.entry["bg"] = "black"
		self.entry.pack(fill=X,pady=0)
		self.entry.bind("<Key-Return>", self.SendMessage)
#		self.entry.bind("<Key-Tab>", lambda _: self.entry.insert(INSERT, "\t"))
	def SendMessage(self, event):
		data = self.entry.get()
		self.entry.delete(0, END)
		self.conn.OnCommand(data, self.OnResult)
		self.ReceiveMessage(self.prompt + data)	# echo
	def ReceiveMessage(self, data):
		self.text.config(state=NORMAL)
		self.text.insert(END, data+"\n")
		self.text.config(state=DISABLED)
		self.text.yview_pickplace('end')
	def OnResult(self, more):
		if more:
			self.prompt = '... '
		else:
			self.prompt = '>>> '

# install reactor support for Tk
root = Tk()
tksupport.install(root)

root.title("Admin Terminal")
terminal = Terminal(root)

reactor.run()
