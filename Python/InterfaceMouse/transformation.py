from numpy import matrix
from numpy.linalg import inv
from numpy.linalg import cond
from goToPosition import GoToPos

def getTransformationMat(A):
	B = matrix([[-10,25,8.7,1],[0,21.22,12.86,1],[0,36,8.7,1],[10,21,15,1],[-15,31,20,1],[10,31,20,1],[10,29,15,1],[15,29,15,1],[-15,20,15,1],[-10,20,15,1],[3,18,5,1],[5,20,25,1],[-5,25,25,1],[-5,30,6,1],[15,20,6,1]]) #Arm Frame
	B = B.transpose()
	C = B * (A.transpose()) * inv(A * (A.transpose()))
	print cond(C)
	return C