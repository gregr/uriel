# Gregory Rosenblatt
# 3/18/06

from clientutil import *
import uriel.playersenses as senses
from uriel.gui.widget import *
from uriel.graphics import renderer, openglrenderer
from uriel.core.functionmap import MakeFunctionMap
from OpenGL.GL import *


LoadImage = renderer.LoadImage

class InputBox(Widget):
	def __init__(self, parent, font, modetext, pos=(0,0)):
		Widget.__init__(self, parent, pos)
		self.font = font
		self.inputtext = InputText(font)
		self.SetModeText(modetext)
	def SetModeText(self, text):
		self.modetext = text#self.font.render(text, 1, (255,255,0))##
	def OnDraw(self):
		x, y = self.rect.topleft
		font = self.font
		glColor3f(1.0,1.0,0.0)
		font.DrawString(self.modetext, (x,y))
		glColor3f(1.0,1.0,1.0)
		font.DrawString(self.inputtext.value, (x, y+font.font.get_linesize()))
#		screen = pygame.display.get_surface()##
#		screen.blit(self.modetext, (x, y))##
#		screen.blit(self.inputtext.text, (x, y+self.font.get_linesize()))##

class MessageBox(Widget):
	def __init__(self, parent, font, pos=(0,0)):
		Widget.__init__(self, parent, pos)
		self.font = font
		self.history = MessageHistory(font)
		self.lineHeight = font.font.get_linesize()
	def OnDraw(self):
#		screen = pygame.display.get_surface()
		lineHeight = self.lineHeight
		yoffset = 0
		font = self.font
		glColor3f(0.0,0.75,1.0)
		for text in self.history.lines:
			font.DrawString(text, (0, yoffset))
#			screen.blit(text, (0, yoffset))##
			yoffset += lineHeight
		glColor3f(1.0,1.0,1.0)

tilesize = 32
numCharacterClothings = 8
numCharacterOrients = 4
numCharacterFrames = 2

charImageName = 'data/characters.bmp'

class CharacterDrawer:
	def __init__(self):	
		self.images = [[[LoadImage(charImageName, True
					,((o*2+f)*tilesize, c*tilesize, tilesize, tilesize))
					for f in xrange(numCharacterFrames)]
					for o in xrange(numCharacterOrients)]
					for c in xrange(numCharacterClothings)]
	def Draw(self, entity, pos):
		self.images[entity.clothing][entity.orient][entity.animFrame].Draw(pos)

numFloorColors = 12
numFloorColumns = 6

floorImageName = 'data/floors.bmp'

class FloorDrawer:
	def __init__(self):
		self.images = [LoadImage(floorImageName, None
						,(c%numFloorColumns*tilesize
						,int(c/numFloorColumns)*tilesize
						,tilesize, tilesize))
						for c in xrange(numFloorColors)]
	def Draw(self, floor, pos):
		self.images[floor.color].Draw(pos)

numStatueOrients = 2

statueImageName = 'data/statues.bmp'

class StatueDrawer:
	def __init__(self):
		self.images = [LoadImage(statueImageName, True
						,(o*tilesize, 0, tilesize, tilesize))
						for o in xrange(numStatueOrients)]
	def Draw(self, statue, pos):
		self.images[statue.orient].Draw(pos)

class View(Widget):
	def __init__(self, parent, font, model, pos=(0,0)):
		Widget.__init__(self, parent, pos)
		self.model = model
		self.identity = None	# identity associated with this view
		self.font = font
		self.characterDrawer = CharacterDrawer()
		self.floorDrawer = FloorDrawer()
		self.statueDrawer = StatueDrawer()
		self.terrainImages = {
					'dirt': LoadImage('data/dirt.bmp'),
					'grass': LoadImage('data/grass.bmp'),
					'swamp': LoadImage('data/swamp.bmp'),
					'water': LoadImage('data/water.bmp'),
					'mountain': LoadImage('data/mountain.bmp'),
					'lava': LoadImage('data/lava.bmp'),
					'void': LoadImage('data/void.bmp')}
#		self.tilesize = 32
		self.visualrange = senses.visualRange
	def OnDraw(self):
		model = self.model
		entities = model.entities
		identity = self.identity
		if identity not in entities:
			return
		space = model.spaces[entities[identity].space]
		xpos, ypos = self.rect.topleft
		visualrange = self.visualrange
		diameter = visualrange+visualrange+1
#		tilesize = self.tilesize
		xref,yref,zref = entities[identity].sector
		xref -= visualrange
		yref -= visualrange
		zref -= visualrange
		for z in xrange(diameter):
			for y in xrange(diameter):
				for x in xrange(diameter):
					index = (x+xref, y+yref, z+zref)
					if index in space:
						cx, cy = (xpos + x*tilesize), (ypos + y*tilesize)
						sector = space[index]
						self.DrawSector(sector.terrain, cx, cy)
						for id in sector.entities:
							self.DrawEntity(entities[id], cx, cy)
	def DrawSector(self, terrain, xpos, ypos):
		if terrain:
			self.terrainImages[terrain].Draw((xpos, ypos))
#			pygame.display.get_surface().blit(self.terrainimages[terrain]##
#											,(xpos, ypos))

	entityDrawHandlers, entitydrawhandler = MakeFunctionMap()

	def DrawEntity(self, entity, xpos, ypos):
		if entity.type in self.entityDrawHandlers:
			self.entityDrawHandlers[entity.type](self, entity, xpos, ypos)

	@entitydrawhandler("perceiver")
	def DrawCharacter(self, entity, xpos, ypos):#, nameImages={}):
#		screen = pygame.display.get_surface()##
		self.characterDrawer.Draw(entity, (xpos, ypos))
		font = self.font
		glColor3f(1.0,0.0,0.0)
		font.DrawString(entity.name, (xpos, ypos-font.font.get_linesize()))
		glColor3f(1.0,1.0,1.0)
#		tilesize = self.tilesize
#		screen.blit(self.charimage, (xpos, ypos)##
#					,Rect(((entity.orient*2+int(entity.animFrame))*tilesize
#						,entity.clothing*tilesize)
#						,(tilesize, tilesize)))
#		if entity.name not in nameImages:
#			nameImages[entity.name] = font.render(entity.name, 1, (255,0,0))
#		screen.blit(nameImages[entity.name]##
#					,(xpos, ypos-self.font.get_linesize()))

	@entitydrawhandler("statue")
	def DrawStatue(self, entity, xpos, ypos):
		self.statueDrawer.Draw(entity, (xpos, ypos))
#		screen = pygame.display.get_surface()##
#		tilesize = self.tilesize
#		screen.blit(self.statueimage, (xpos, ypos)##
#					,Rect((entity.orient*tilesize, 0)
#						,(tilesize, tilesize)))

	@entitydrawhandler("floor")
	def DrawFloor(self, entity, xpos, ypos):
		self.floorDrawer.Draw(entity, (xpos, ypos))
#		screen = pygame.display.get_surface()##
#		tilesize = self.tilesize
#		row = int(entity.color / 6)
#		column = entity.color % 6
#		screen.blit(self.floorimage, (xpos, ypos)##
#					,Rect((column*tilesize, row*tilesize)
#						,(tilesize, tilesize)))
