# Gregory Rosenblatt
# 2/6/06

from uriel.core.enum import *

# specialized signal data
#					name						args
signalTypes = Enum([#"new_resource",				# sector, resource
					#"del_resource",				# sector, resource
					"terrain_change",			# sector, terrain
					"new_entity",				# entity
					"del_entity",				# entity, oldpos
					"depart",					# entity, oldpos
					"arrive",					# entity, oldpos
					"entity_state_change",		# entity, fields
					"action",					# entity, actiontype
					"talk",						# entity, message
					"whisper"					# entity, message
					])

# make this a resource state change of some type instead
# and notify sensors that detect mineral changes... or something
#def NewResourceSignal(sector, resource):
#	return (mediums.mineral, [signalTypes.new_resource
#								,(sector, resource)]
#			,[sector])

#def DelResourceSignal(sector, resource):
#	return (mediums.mineral, [signalTypes.del_resource
#								,(sector, resource)]
#			,[sector])

def TerrainChangeSignal(mediums, sector, terrain):
	return (mediums, [signalTypes.terrain_change
								,(sector, terrain)]
			,[sector])

def NewEntitySignal(mediums, entity):
	return (mediums, [signalTypes.new_entity, entity]
			,[entity.sector])

def DelEntitySignal(mediums, entity, oldpos):
	return (mediums, [signalTypes.del_entity, (entity, oldpos)]
			,[oldpos])

def DepartSignal(mediums, entity, oldpos):
	return (mediums, [signalTypes.depart, (entity, oldpos)]
			,[oldpos])

def ArriveSignal(mediums, entity, oldpos):
	return (mediums, [signalTypes.arrive, (entity, oldpos)]
			,[entity.sector])

def EntityStateChangeSignal(mediums, entity, change):
	return (mediums, [signalTypes.entity_state_change
								,(entity, change)]
			,[entity.sector])

def ActionSignal(mediums, entity, action):
	return (mediums, [signalTypes.action, (entity, action)]
			,[entity.sector])

def TalkSignal(mediums, entity, message):
	return (mediums, [signalTypes.talk, (entity, message)]
			,[entity.sector])
