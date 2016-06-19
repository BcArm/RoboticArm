#import the necessary modules
import time
import freenect
import cv2
import numpy as np
import math
from goToPosition import GoToPos
from getGripperCenter import getGripperCenter
from callibration import getTransformationMat
from goToPosDrawLine import DrawLineGoToPos

capture = cv2.VideoCapture()
real = None

TRANS_MAT = np.matrix([])

ITR = 20

def get_position(x, y):
	print x,y	
	xw, yw, zw = 0, 0, 0
	for i in range(ITR):
		capture.grab()
		ok, real = capture.retrieve(0, cv2.CAP_OPENNI_POINT_CLOUD_MAP)
		xw += 100 * real[x][y][0]
		yw += 100 * real[x][y][1]
		zw += 100 * real[x][y][2]
	xw /= ITR
	yw /= ITR
	zw /= ITR
        print xw, yw, zw
	return [xw, yw, zw]

def go_to_position_mouse(event, y, x, flags, param):
    global TRANS_MAT
    if event == cv2.EVENT_LBUTTONDOWN:
        pos = get_position(x,y)    
        
        xk = pos[0]
        yk = pos[1]
        zk = pos[2]

        print xk, yk, zk

        point = TRANS_MAT * np.matrix([[xk],[yk],[zk],[1]])
	
    	print point[0],point[1],point[2]
        GoToPos(point[0],point[1],point[2],'open')
        '''
        DrawLineGoToPos(0,21.22,12.86,point[0],point[1],point[2],'open',[111.628,70.866,-65.91],5)
        time.sleep(7)
        GoToPos(0,21.22,12.86,'close')
        '''
		

#function to get coordinates of gripper center with respect to kinect frame
def  get_kinect_frame_pt():
	capture.grab()
	ok, frame = capture.retrieve(0, cv2.CAP_OPENNI_BGR_IMAGE)
        if not ok:
            print "HERE"
        gripper_centerXY = getGripperCenter(frame)
        return get_position(gripper_centerXY[0],gripper_centerXY[1])

cv2.namedWindow('RGB image')

if __name__ == "__main__":
	#callibrate kinect
    capture.open(cv2.CAP_OPENNI2)
    if (capture.isOpened() == False):
        capture.open(cv2.CAP_OPENNI)
    kinect_frame_pts = []

    GoToPos(-10,25,8.7,'close')
    time.sleep(5)
    kinect_frame_pts.append(get_kinect_frame_pt())
    
    GoToPos(0,21.22,12.86,'close')
    time.sleep(5)
    kinect_frame_pts.append(get_kinect_frame_pt())
        
    GoToPos(0,36,8.7,'close')
    time.sleep(5)
    kinect_frame_pts.append(get_kinect_frame_pt())
    
    GoToPos(10,21,15,'close')
    time.sleep(5)
    kinect_frame_pts.append(get_kinect_frame_pt())

    GoToPos(-15,31,20,'close')
    time.sleep(5)
    kinect_frame_pts.append(get_kinect_frame_pt())

    GoToPos(10,31,20,'close')
    time.sleep(5)
    kinect_frame_pts.append(get_kinect_frame_pt())

    GoToPos(10,29,15,'close')
    time.sleep(5)
    kinect_frame_pts.append(get_kinect_frame_pt())

    GoToPos(15,29,15,'close')
    time.sleep(5)
    kinect_frame_pts.append(get_kinect_frame_pt())

    GoToPos(-15,20,15,'close')
    time.sleep(5)
    kinect_frame_pts.append(get_kinect_frame_pt())

    GoToPos(-10,20,15,'close')
    time.sleep(5)
    kinect_frame_pts.append(get_kinect_frame_pt())

    GoToPos(3,18,5,'close')
    time.sleep(5)
    kinect_frame_pts.append(get_kinect_frame_pt())

    GoToPos(5,20,25,'close')
    time.sleep(5)
    kinect_frame_pts.append(get_kinect_frame_pt())

    GoToPos(-5,25,25,'close')
    time.sleep(5)
    kinect_frame_pts.append(get_kinect_frame_pt())

    GoToPos(-5,30,6,'close')
    time.sleep(5)
    kinect_frame_pts.append(get_kinect_frame_pt())
    
    GoToPos(15,20,6,'close')
    time.sleep(5)
    kinect_frame_pts.append(get_kinect_frame_pt())

    Kinect_frame_matrix = np.matrix([[kinect_frame_pts[0][0],kinect_frame_pts[0][1],kinect_frame_pts[0][2],1],\
                                    [kinect_frame_pts[1][0],kinect_frame_pts[1][1],kinect_frame_pts[1][2],1],\
                                    [kinect_frame_pts[2][0],kinect_frame_pts[2][1],kinect_frame_pts[2][2],1],\
                                    [kinect_frame_pts[3][0],kinect_frame_pts[3][1],kinect_frame_pts[3][2],1],\
                                    [kinect_frame_pts[4][0],kinect_frame_pts[4][1],kinect_frame_pts[4][2],1],\
                                    [kinect_frame_pts[5][0],kinect_frame_pts[5][1],kinect_frame_pts[5][2],1],\
                                    [kinect_frame_pts[6][0],kinect_frame_pts[6][1],kinect_frame_pts[6][2],1],\
                                    [kinect_frame_pts[7][0],kinect_frame_pts[7][1],kinect_frame_pts[7][2],1],\
                                    [kinect_frame_pts[8][0],kinect_frame_pts[8][1],kinect_frame_pts[8][2],1],\
                                    [kinect_frame_pts[9][0],kinect_frame_pts[9][1],kinect_frame_pts[9][2],1],\
                                    [kinect_frame_pts[10][0],kinect_frame_pts[10][1],kinect_frame_pts[10][2],1],\
                                    [kinect_frame_pts[11][0],kinect_frame_pts[11][1],kinect_frame_pts[11][2],1],\
                                    [kinect_frame_pts[12][0],kinect_frame_pts[12][1],kinect_frame_pts[12][2],1],\
                                    [kinect_frame_pts[13][0],kinect_frame_pts[13][1],kinect_frame_pts[13][2],1],\
                                    [kinect_frame_pts[14][0],kinect_frame_pts[14][1],kinect_frame_pts[14][2],1],\
                                    ])

    TRANS_MAT = getTransformationMat(Kinect_frame_matrix)

    cv2.setMouseCallback('RGB image', go_to_position_mouse)

    while 1:
        if not capture.grab():
            print "Unable to grab frame from kinect"
            break

        ok, rgb = capture.retrieve(0, cv2.CAP_OPENNI_BGR_IMAGE)
        if not ok:
            print "Unable to retrieve RGB image"
            break
        cv2.imshow('RGB image', rgb)

        ok, depth = capture.retrieve(0, cv2.CAP_OPENNI_DISPARITY_MAP)
        if not ok:
            print "Unable to retrieve depth map"
            break
        cv2.imshow('Depth map', depth)

        # quit program when 'esc' key is pressed
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break;
    cv2.destroyAllWindows()
