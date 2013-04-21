# Gregory Rosenblatt
# 2/8/06

class Struct:
	"""An anonymous structure factory."""

	def __init__(self, **attributes):
		"""Create an anonymous structure with the given attributes."""
		self.__dict__.update(attributes)
