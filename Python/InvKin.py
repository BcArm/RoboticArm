import math
import numpy as np
from scipy.optimize import fsolve
from scipy.optimize import root
from scipy.optimize import least_squares
from forwardKinematics import forwardKinematics
def invKin(x,y,z,guess): #T
	z = z-2.5 #Eliminate the effect of the base on z coordinate
	th5 = 0 #theta 5 is not used
	th1 = math.atan2(math.fabs(y),math.fabs(x)) #Get theta 1 
	th1 = np.rad2deg(th1) #convert theta 1 to degrees
	if (y == 0 and x == 0):
		th1 = 0
	elif (x == 0):
		if (y > 0):
			th1 = 90
		else:
			th1 = -90
	elif (y/x < 0): 
		th1 = 180 - th1
	th1 = np.deg2rad(th1) #convert theta 1 to radians
	guess[2] = guess[2] - 90 #convert theta4 from arm angle to DH frame angle
	#convert guess to radians
	guess[0] = np.deg2rad(guess[0]) 
	guess[1] = np.deg2rad(guess[1])
	guess[2] = np.deg2rad(guess[2])
	sApproach = 1.05
	angles = [1,2,3,4,5,0]

	#Solve euations to get th2,th3,th4
	def solveFn(r):
		th2 = r[0]
		th3 = r[1]
		th4 = r[2]
		f = np.zeros(3)
		f[0] = math.cos(th2-th3+th4) - sApproach
		f[1] = 4*math.sin(th1)*( 2*math.cos(th2 - th3) - 5*math.sin(th2 - th3 + th4) + 2*math.cos(th2) )-y
		f[2] = 8*math.sin(th2 - th3) + 20*math.cos(th2 - th3 + th4) + 8*math.sin(th2) + (31/5)-z
		return f

	#Compare coordinates resulted from computed angles with real coordinates
	def check(x1,x2,x3,x4,x5):
		t1 = forwardKinematics(x1,x2,x3,x4,x5)
		t1 = t1[:,3]
		t2 = [x,y,z,1]
		e = abs( t2 - t1 )
		if( e[0] < 0.3 and e[1] < 0.3 and e[2] < 0.3 ):
			flag = 1
		else:
			flag = 0
		return flag

	for i in range (0,41):
		sApproach = sApproach - 0.05
		obj = least_squares(solveFn, guess, bounds = ([np.deg2rad(-7), np.deg2rad(-102), np.deg2rad(-97-90)], [np.deg2rad(181), np.deg2rad(81), np.deg2rad(86-90)]), method = 'dogbox')
		#obj = root(solveFn, guess, method='lm')
		r = obj.x
		flag = check(th1,r[0],r[1],r[2],th5)
		if (flag):
			theta1 = np.rad2deg(th1) - 90
			th2 = np.rad2deg(r[0])
			th3 = np.rad2deg(r[1])
			th4 = np.rad2deg(r[2]) + 90
			if((theta1 <= 90) and (theta1 >= -85)):
				if((th2 <= 181) and (th2 >= -7)):
					if((th3 <= 81) and (th3 >= -102)):
						if((th4 <= 86) and (th4 >= -97)):
							angles = np.vstack((angles,[theta1,th2,th3,th4,th5,sApproach]))

	if( angles.shape[0] > 2 ):
		guess[0] = np.rad2deg(guess[0]) 
		guess[1] = np.rad2deg(guess[1])
		guess[2] = np.rad2deg(guess[2])
		prevThetas = [theta1,guess[0],guess[1],guess[2]+90];
		nearest = angles[1,:]
		diff1 = (prevThetas[0] - nearest[0])**2
		diff2 = (prevThetas[1] - nearest[1])**2
		diff3 = (prevThetas[2] - nearest[2])**2
		diff4 = (prevThetas[3] - nearest[3])**2
		D = diff1 + diff2 + diff3 + diff4
		D = math.sqrt(D)
		minD = D  
		for i in range(2,angles.shape[0]):
			current = angles[i,:]
			diff1 = (prevThetas[0] - current[0])**2
			diff2 = (prevThetas[1] - current[1])**2
			diff3 = (prevThetas[2] - current[2])**2
			diff4 = (prevThetas[3] - current[3])**2
			D = diff1 + diff2 + diff3 + diff4
			D = math.sqrt(D)
			if( D < minD ):
				minD = D;
				nearest = current		
		angles = nearest;
	elif(angles.shape[0] == 2):
		angles = angles[1,:]
	else:
		print'No solution can be found'

	return np.round(angles,decimals=1)
#print(invKin(-10,25,8.7,[0,0,0]))