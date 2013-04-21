# Gregory Rosenblatt
# 4/9/06

from weakref import ref


def WeakMethod(method, *early_args, **early_kwargs):
	"""Create a bound method that does not prevent garbage collection.
		
	Optional arguments may be stored for later invocation of the method.
	"""
	selfRef = ref(method.im_self)
	m = method.im_func
	if args:
		if kwargs:
			def method_proxy(*args, **kwargs):
				kw = early_kwargs.copy()
				kw.update(kwargs)
				m(selfRef(), *(early_args+args), **kw)
		else:
			def method_proxy(*args, **kwargs):
				m(selfRef(), *(early_args+args), **kwargs)
	elif kwargs:
		def method_proxy(*args, **kwargs):
			kw = early_kwargs.copy()
			kw.update(kwargs)
			m(selfRef(), *args, **kw)
	else:
		def method_proxy(*args, **kwargs):
			m(selfRef(), *args, **kwargs)
	return method_proxy
