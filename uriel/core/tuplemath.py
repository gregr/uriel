# Gregory Rosenblatt
# 12/8/05

# some basic operations that treat tuples as vectors

def Add2d(t, t0):	# vector addition of t and t0
	i,j, = t
	x,y = t0
	return (i+x, j+y)

def Add3d(t, t0):
	i,j,k = t
	x,y,z = t0
	return (i+x, j+y, k+z)

def Subtract2d(t, t0):	# diff between vector t and its reference origin t0
	i,j = t
	x,y = t0
	return (i-x, j-y)

def Subtract3d(t, t0):
	i,j,k = t
	x,y,z = t0
	return (i-x, j-y, k-z)

def Scale2d(t, s):	# scale by factor s
	i,j = t
	return (i*s, j*s)

def Scale3d(t, s):
	i,j,k = t
	return (i*s, j*s, k*s)

def IntegerScale2d(t, s):	# scale by factor s
	i,j = t
	return (int(i*s), int(j*s))

def IntegerScale3d(t, s):
	i,j,k = t
	return (int(i*s), int(j*s), int(k*s))

def Mod2d(t, s):	# apply modulus of s
	i,j = t
	return (i%s, j%s)

def Mod3d(t, s):
	i,j,k = t
	return (i%s, j%s, k%s)

def ReverseCmp2d(t1, t2):	# compare with reversed element significance
	x1,y1 = t1
	x2,y2 = t2
	if y1 > y2:
		return -1
	elif y1 == y2:
		return cmp(x1, x2)
	return 1

def ReverseCmp3d(t1, t2):
	x1,y1,z1 = t1
	x2,y2,z2 = t2
	if z1 > z2:
		return -1
	elif z1 == z2:
		if y1 > y2:
			return -1
		elif y1 == y2:
			return cmp(x1, x2)
	return 1
