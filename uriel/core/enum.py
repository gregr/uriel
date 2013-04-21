# Gregory Rosenblatt
# 2/8/06

class Enum:
	"""A collection of enumerated names."""

	def __init__(self, names):
		"""Enumerate the given names and store as attributes."""
		self.names = names
		self.numVals = len(names)
		map(self.__dict__.__setitem__, names, xrange(self.numVals))

	def __add__(self, names):
		"""__add__(names) -> Enum
			
		Return a copy of this enumeration with additional enumerated names.
		"""
		return Enum(self.names + names)
