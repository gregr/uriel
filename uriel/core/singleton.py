# Gregory Rosenblatt
# 4/12/06

from weakref import WeakValueDictionary


def IsSingleton(obj, instances=WeakValueDictionary()):
	"""Assert that the class of obj has not already been instantiated."""
	if obj.__class__ in instances:
		return False
	instances[obj.__class__] = obj
	return True
