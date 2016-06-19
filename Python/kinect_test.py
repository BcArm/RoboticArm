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

        #cv2.imshow('Depth image', depth.astype(np.uint8))
        
        zw = 1 / ( ( (depth[y][x])*-0.0030711016 )+ 3.3309495161 )
        zw = 100 * zw
        sumz = sumz + zw
        fx = 640 / (2 * math.tan(math.radians(57 / 2)))
        xw = zw * (x - 319) / fx
        sumx = sumx + xw
        fy = 480 / (2 * math.tan(math.radians(43 / 2)))
        yw = zw * (y - 239) / fy
        sumy = sumy + yw
    print sumx/20, sumy/20, sumz/20
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
        print point[0],point[1],point[2]
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
    print Kinect_frame_matrix.transpose()
    TRANS_MAT = getTransformationMat(Kinect_frame_matrix.transpose())
    
    print TRANS_MAT

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