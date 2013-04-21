# Gregory Rosenblatt
# 4/12/06

from weakref import WeakValueDictionary


class Resource(type):
	"""A metaclass for managed-resource classes.
		
	Classes using this metaclass should not already define '_pool_'.
	"""

	def __init__(cls, name, bases, dict):
		"""Add a pool to the class to track existing resources."""
		super(Resource, cls).__init__(name, bases, dict)
		cls._pool_ = WeakValueDictionary()

	def __call__(cls, *args):
		"""Retrieve the resource described by the given args.
			
		A new resource instance will only be created if the appropriate one
		does not already exist in the pool.
		"""
		pool = cls._pool_
		if args in pool:
			self = pool[args]
		else:
			self = cls.__new__(cls, *args)
			self.__init__(*args)
			pool[args] = self
		return self


def _Test():
	import unittest
	class Res(object):
		__metaclass__ = Resource
		def __init__(self, *args):
			self.args = tuple(args)
	class TestResource(unittest.TestCase):
		def test_identity_and_pool(self):
			argv = (1, 2, "three")
			a = Res(*argv)
			aa = Res(*argv)
			self.assert_(a is aa)	# should be the same object
			self.assert_(Res._pool_)	# pool should not be empty
			del a
			del aa
			self.assert_(not Res._pool_)	# pool should be empty
	return unittest.makeSuite(TestResource)


if __name__ == "__main__":
	import unittest
	result = unittest.TextTestRunner(verbosity=2).run(_Test())
	print result.wasSuccessful()


# for non-class resources
def MakeResource(args, construct, pool):
	"""Provide a resource determined by the given arguments and constructor.
		
	Constructed resources are stored in the given pool by argument index.
	If the resource already exists in the pool, it will be returned.
	args - The arguments used to construct the resource and as the key.
	construct - The constructor used to create new resources.
	pool - A dictionary containing the currently loaded resource instances.
	"""
	if args in pool:
		return pool[args]
	res = construct(*args)
	pool[args] = res
	return res


#class Resource(object):
#	"""A resource class that only constructs unique instances.
#		
#	Resource instances are indexed by their construction arguments and stored
#	in a class pool for reuse.  If an attempt is made to create a resource
#	with an argument index that already exists, the existing resource is
#	referenced rather than constructing a new one.
#
#	Subclasses must override Construct and define a pool (WeakValueDictionary).
#	"""
#	def __new__(cls, *args):
#		obj = cls.pool.get(args, None)
#		if not obj:
#			obj = object.__new__(cls)
#			obj.__construct__(*args)
#			cls.pool[args] = obj
#		return obj
#	def __construct__(self, *args):
#		raise NotImplementedError

#from weakref import WeakValueDictionary

#class Test(Resource):
#	pool = WeakValueDictionary()
#	def Construct(self, value):
#		self.value = value
#		print "created:", self.value
#	def __del__(self):
#		print "destroyed:", self.value
