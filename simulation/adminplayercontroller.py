# Gregory Rosenblatt
# 3/12/06

from playercontroller import PlayerController
from entitycontroller import EntityController
from entity import Entity
from uriel.core.process import Process
from uriel.core.functionmap import ExtendFunctionMap
from weakref import WeakValueDictionary


class AdminPlayerController(PlayerController):
	""""""

	controlledEntities = WeakValueDictionary()

	commandTypes = (PlayerController.commandTypes
					+[
						"take_control",
						"restore_control",
						"command_entity"
					])

	commands, commandhandler = ExtendFunctionMap(PlayerController.commands)

	@commandhandler(commandTypes.take_control)
	def OnTakeControl(self, ident):
		if ((ident not in self.controlledEntities) and (ident in Entity.pool)
				and (id(self.entity) != ident)):
			# also add restrictions to prevent admins from being possessed?
			# maybe not necessary, since an admin can also restore his control
			# or use his own adminController when taken control of
			target = Entity.pool[ident]
			if hasattr(target, "controller"):	# controllable?
				del target.controller.process	# first neuter the target
				target.adminController = EntityController(target) # install new
				self.controlledEntities[ident] = target

	@commandhandler(commandTypes.restore_control)
	def OnRestoreControl(self, ident):
		if ident in self.controlledEntities:
			target = self.controlledEntities[ident]
			del target.adminController
			target.controller.process = Process(target.controller.Executer())
			del self.controlledEntities[ident]

	@commandhandler(commandTypes.command_entity)
	def OnCommandEntity(self, ident, type, args):
		if ident in self.controlledEntities:
			target = self.controlledEntities[ident]
			controller = target.adminController
			if type in controller.actionQueues:
				controller.OnAction((type, args))
