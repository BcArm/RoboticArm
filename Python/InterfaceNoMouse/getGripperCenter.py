import cv2
import numpy as np
def getGripperCenter(frames):
	assert(len(frames) > 0)
	n = frames[0].shape[0]
	m = frames[0].shape[1]
	sumX = 0
	sumY = 0
	cnt = 0
	out = frames[0].copy()
	ind = frames[0].copy()
	bestVal, a, b = 0, 0, 0
	for x in xrange(n):
		for y in xrange(m):
			lst = int(frames[0][x, y, 2])
			val = 0
			for item in frames:
				if (abs(lst - int(item[x, y, 2])) > 10):
					val += abs(lst - int(item[x, y, 2]))
				lst = int(item[x, y, 2])

			if (val > bestVal):
				bestVal = val
				a = x
				b = y
	result = (a, b)
	#cv2.imshow("Indication", ind)
	return result
