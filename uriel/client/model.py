# Gregory Rosenblatt
# 2/8/06

from uriel.core.struct import *
#from weakref import proxy

# expand with line of sight calcs
def GetSectorsInRange(sector, range):
	x,y,z = sector
	rangeplusone = range+1
	sectors = set()
	for k in xrange(max(0, z-range), z+rangeplusone):
		for j in xrange(max(0, y-range), y+rangeplusone):
			for i in xrange(max(0, x-range), x+rangeplusone):
				sectors.add((i,j,k))
	return sectors

class Model:
	def __init__(self):#, controller):
#		self.controller = proxy(controller)
		self.spaces = {}	# start using this to organize sectors
		self.entities = {}
	def OnNewSectorGroup(self, sectors):
		space = sectors.pop()
		if space not in self.spaces:
			self.spaces[space] = {}	# new sector mapping
		for data in sectors:
			data = [space] + list(data)
			self.OnNewSector(data)
	def OnNewSector(self, data):
		space, index, terrain = data
		self.spaces[space][index] = Struct(terrain=terrain
										,entities=set())
	def OnTerrainChange(self, data):
		space, index, terrain = data
		self.spaces[space][index].terrain = terrain
#	def OnNewResource(self, data):
#		space, index, resource = data
#		self.spaces[space][index].resources[resource] = None
#	def OnDelResource(self, data):
#		space, index, resource = data
#		resources = self.spaces[space][index].resources
#		if resource in resources:
#			del resources[resource]
	def OnNewEntityGroup(self, entities):
		space = entities.pop()
		for data in entities:
			data = [space] + list(data)
			self.OnNewEntity(data)
	def OnNewEntity(self, data):
		space, ident, state = data
		sector = state['sector']
		state['space'] = space
		state['animFrame'] = sum(sector) % 2	# 2 animation frames
		if ident in self.entities:
			oldEntity = self.entities[ident]
			oldSector = self.spaces[oldEntity.space][oldEntity.sector]
			oldSector.entities.discard(ident)
		self.entities[ident] = Struct(**state)
		try:
			space = self.spaces[space]
			if sector in space:
				space[sector].entities.add(ident)
			else:
				space[sector] = Struct(terrain=None, entities=set([ident]))
		except:
			print "new entity error, sector!!!@$@$#$%"
			raise
	def OnDelEntity(self, ident):
		entity = self.entities[ident]
		space, sector = self.spaces[entity.space], entity.sector
		space[sector].entities.remove(ident)	# it should be there
	def OnDepart(self, ident):	# maybe a movement animation later?
		entity = self.entities[ident]
		space, sector = self.spaces[entity.space], entity.sector
		space[sector].entities.remove(ident)	# it should be there (discard)
	def OnArrive(self, data):
		ident, newpos = data
		try:
			entity = self.entities[ident]
		except:
			print "arrive error, entity"
			raise
		space = self.spaces[entity.space]
		entity.sector = newpos
		entity.animFrame = not entity.animFrame
		if newpos in space:
			space[newpos].entities.add(ident)
		else:
			space[newpos] = Struct(terrain=None, entities=set([ident]))
	def OnEntityStateChange(self, data):
		ident, change = data
		try:
			self.entities[ident].__dict__.update([change])	# update state
		except:
			print "state error, entity"
			raise
