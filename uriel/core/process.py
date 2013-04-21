# Gregory Rosenblatt
# 3/12/06

from uriel.core.struct import Struct
from weakref import proxy


def ProcessUpdater(group):
	"""Perform an iteration for each process in the given group."""
	processes = group.processes
	addedProcesses = group.addedProcesses
	removedProcesses = group.removedProcesses
	del group	# don't imprison references in this generator
	while True:
		if addedProcesses:
			processes |= addedProcesses
			addedProcesses.clear()
		if removedProcesses:
			processes -= removedProcesses
			removedProcesses.clear()
		for p in processes:
			try:
				p.next()
			except StopIteration:
				removedProcesses.add(p)
		p = None	# don't imprison references in this generator
		yield None


def ProcessGroup(target=None):
	"""Create a new process group or adapt a target to behave as one."""
	if target is None:
		target = Struct()
	target.processes = set()
	target.addedProcesses = set()
	target.removedProcesses = set()
	target.updater = ProcessUpdater(proxy(target))
	return target


_mainGroup = ProcessGroup()


class Process(object):
	"""An automatically managed iterative process."""

	__slots__ = ["process", "group"]
	updater = _mainGroup.updater

	def __init__(self, process, group=_mainGroup):
		"""Create a managed process in the given group."""
		self.group = group
		self.process = process
		group.addedProcesses.add(process)

	def __del__(self):
		"""Remove the managed process from its group."""
		self.group.removedProcesses.add(self.process)


def AddProcess(process, group=_mainGroup):
	"""Add an unmanaged iterative process to the given group."""
	group.addedProcesses.add(process)
