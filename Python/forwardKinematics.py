import math
import numpy as np

def forwardKinematics(th1,th2,th3,th4,th5):
	T=np.array([[math.cos(th2-th3+th4)*math.cos(th1)*math.cos(th5)-math.sin(th1)*math.sin(th5),-math.cos(th5)*math.sin(th1)-math.cos(th2-th3+th4)*math.cos(th1)*math.sin(th5),-math.sin(th2-th3+th4)*math.cos(th1),4*math.cos(th1)*(2*math.cos(th2-th3)-5*math.sin(th2-th3+th4)+2*math.cos(th2))],

	[math.cos(th2-th3+th4)*math.sin(th1)*math.cos(th5)+math.cos(th1)*math.sin(th5),math.cos(th5)*math.cos(th1)-math.cos(th2-th3+th4)*math.sin(th1)*math.sin(th5),-math.sin(th2-th3+th4)*math.sin(th1),4*math.sin(th1)*(2*math.cos(th2-th3)-5*math.sin(th2-th3+th4)+2*math.cos(th2))],

	[math.sin(th2-th3+th4)*math.cos(th5),-math.sin(th2-th3+th4)*math.sin(th5),math.cos(th2-th3+th4),8*math.sin(th2-th3)+20*math.cos(th2-th3+th4)+8*math.sin(th2)+31.0/5.0],

	[0,0,0,1]],np.float)
	
	return np.round(T,decimals=2)


