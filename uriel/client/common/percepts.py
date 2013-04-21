# Gregory Rosenblatt
# 1/11/06

from uriel.core.enum import *

# the client has to know about these enumerations somehow
# include a system message percept? (admin announcements or private msgs?)
					# type						# data
perceptTypes = Enum(["new_commands",			# list of command names
					"new_identity",				# id
					"del_identity",				# id
					"new_sector_group",			# list of new_sector, space
					"new_sector",				# space, index, resources
#					"new_resource",				# space, index, resource
#					"del_resource",				# space, index, resource
					"terrain_change",			# space, index, terrain
					"new_entity_group",			# list of new_entity, space
					"new_entity",				# space, id, state
					"del_entity",				# id
					"depart",					# id
					"arrive",					# id, newpos
					"entity_state_change",		# id, change (name, val)
					"action",					# id, actiontype
					"sound",
					"talk",						# id, message
					"whisper"					# id, message (i think...)
					])
