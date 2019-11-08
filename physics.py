
def gotCollision (posA, posB):
	if (posA.left - posB.width < posB.left and posB.left < posA.left + posA.width) \
		and (posA.top - posA.height < posB.top and posB.top < posA.top + posA.height):
		return True
	else:
		return False
