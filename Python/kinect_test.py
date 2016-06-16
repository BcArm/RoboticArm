import time
import freenect
import cv2
import numpy as np
import math
from goToPosition import GoToPos
from getGripperCenter import getGripperCenter
from callibration import getTransformationMat

depth = []
TRANS_MAT = np.matrix([])
cv2.namedWindow('RGB image')

def get_position(x, y):

    sumx = 0
    sumy = 0
    sumz = 0      
    
    for i in range (0,20):
        get_depth()

        cv2.imshow('RGB image',frame)
        cv2.imshow('Depth image', depth.astype(np.uint8))
        
        zw = 1 / ( ( (depth[y][x])*-0.0030711016 )+ 3.3309495161 )
        zw = 100 * zw
        sumz = sumz + zw
        fx = 640 / (2 * math.tan(math.radians(57 / 2)))
        xw = zw * (x - 319) / fx
        sumx = sumx + xw
        fy = 480 / (2 * math.tan(math.radians(43 / 2)))
        yw = zw * (y - 239) / fy
        sumy = sumy + yw

    return [sumx/20, sumy/20, sumz/20]

def go_to_position_mouse(event, x, y, flags, param):
    
    global TRANS_MAT

    if event == cv2.EVENT_LBUTTONDOWN:
        
        pos = get_position(x,y)    
        
        xk = pos[0]
        yk = pos[1]
        zk = pos[2]

        print xk, yk, zk

        point = TRANS_MAT * np.matrix([[xk],[yk],[zk],[1]])

        GoToPos(point[0],point[1],point[2],'close')

        #print -(zw - 78), xw + 34, -(yw - 4) + 6.2
        #moveObj(-(zw - 78), xw + 34, -(yw - 4) + 6.2)
        #print -(zw - 81), xw + 30, -(yw - 0.5) + 6.7
        #GoToPos(-(zw - 81), xw + 30, -(yw - 0.5) + 6.7, 'open')

#function to get RGB image from kinect
def get_video():
    array,_ = freenect.sync_get_video()
    array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
    return array
 
#function to get depth image from kinect
def get_depth():
    global depth 
    depth, _ = freenect.sync_get_depth()

#function to get coordinates of gripper center with respect to kinect frame
def  get_kinect_frame_pt():
    frame = get_video()
    gripper_centerXY = getGripperCenter(frame)
    gripper_center = get_position(gripper_centerXY[0],gripper_centerXY[1])
    return gripper_center

if __name__ == "__main__":
    
    #callibrate kinect
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
        frame = get_video()
        #get a frame from depth sensor
        get_depth()
        #display RGB image
        cv2.imshow('RGB image',frame)
        #display depth image
        cv2.imshow('Depth image', depth.astype(np.uint8))
 
        # quit program when 'esc' key is pressed
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break;
    cv2.destroyAllWindows()