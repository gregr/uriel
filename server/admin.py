# Gregory Rosenblatt
# 3/12/06

from uriel.net.connection import Connection
from twisted.internet import reactor
import sys

def GetInput(more):
	if more:
		prompt = '... '
	else:
		prompt = '>>> '
	SendCommand(raw_input(prompt))

def SendCommand(data):
	conn.OnCommand(data, GetInput)

def OnUpdate(data):
	print data

def OnConnect():
	print "connection successful"
	GetInput(False)

def OnError():
	print "ERROR!!!!"

configfile = open('adminclientconfig.txt', 'r')
hostname = configfile.readline().strip()
port = int(configfile.readline().strip())
username = configfile.readline().strip()
password = configfile.readline().strip()
del configfile

conn = Connection(hostname, port, username, password
				,OnUpdate, OnConnect, OnError)

try:
	reactor.run()
except KeyboardInterrupt:
	del conn
