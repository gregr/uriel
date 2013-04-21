# Gregory Rosenblatt
# 2/8/06

def MakeFunctionMap():
	"""MakeFunctionMap() -> (funcmap, Mapper)
		
	Create an empty dictionary for mapping keys to functions.
	Returns a dictionary and its mapper (function-decorator) as a tuple.
	"""
	return ExtendFunctionMap({})


def ExtendFunctionMap(funcmap):
	"""ExtendFunctionMap(funcmap) -> (extendedmap, Mapper)
		
	Extend an existing map without modifying the original.
	Returns a dictionary and its mapper (function-decorator) as a tuple.
	"""
	funcmap = funcmap.copy()
	def Mapper(key):
		def Register(func):
			funcmap[key] = func
			return func
		return Register
	return (funcmap, Mapper)
