from numpy import matrix
from numpy.linalg import inv
from goToPosition import GoToPos

def getTransformationMat(A):
	#A = matrix([[1,5,2,7],[1,1,3,31],[1,3,4,17],[1,1,1,1]])
	#B = matrix([[77,75,74,61],[35,39,36,41],[9.2,9.2,7.2,-20.8],[1,1,1,1]])

	#A = matrix([[-7.68,-7.855,-18,-6.24],[5.46,8.912,10.35,5.3816],[110.15,121.22,124.47,129.4126],[1,1,1,1]]) #Kinect Frame
	B = matrix([[-10,0,0,10],[25,21.22,36,21],[8.7,12.86,8.7,15],[1,1,1,1]]) #Arm Frame
	C = B*inv(A)

	#test = matrix([[-5.56606237302],[11.4300619608],[111.661235336],[1]]) 

	#point = C*test 
	#GoToPos(point[0],point[1],point[2],'close')

	#print (C*test)[0]
	return C