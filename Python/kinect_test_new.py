#import the necessary modules
import time
import freenect
import cv2
import numpy as np
import math
from goToPosition import GoToPos
from getGripperCenter import getGripperCenter
from callibration import getTransformationMat

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
    
    Kinect_frame_matrix = np.matrix([[kinect_frame_pts[0][0],kinect_frame_pts[1][0],kinect_frame_pts[2][0],kinect_frame_pts[3][0]],\
                                    [kinect_frame_pts[0][1],kinect_frame_pts[1][1],kinect_frame_pts[2][1],kinect_frame_pts[3][1]],\
                                    [kinect_frame_pts[0][2],kinect_frame_pts[1][2],kinect_frame_pts[2][2],kinect_frame_pts[3][2]],\
                                    [1,1,1,1]])

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
