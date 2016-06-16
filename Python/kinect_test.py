#import the necessary modules
import freenect
import cv2
import numpy as np
import math
from moveObj import moveObj

from getGripperCenter import get getGripperCenter

def get_position(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        sumx = 0
        sumy = 0
        sumz = 0      
        for i in range (0,20):
            get_depth()
            cv2.imshow('RGB image',frame)
            #display depth image
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
        print sumx/20,sumy/20, sumz/20
        #print -(zw - 78), xw + 34, -(yw - 4) + 6.2
        #moveObj(-(zw - 78), xw + 34, -(yw - 4) + 6.2)
        #print -(zw - 81), xw + 30, -(yw - 0.5) + 6.7
        #GoToPos(-(zw - 81), xw + 30, -(yw - 0.5) + 6.7, 'open')
        '''if flag == 1:
            dif[0] = xw
            dif[1] = yw
            dif[2] = zw
        elif flag == 0:
            dif[0] -= xw
            dif[1] -= yw
            dif[2] -= zw
            print dif[0],dif[1],dif[2]'''
depth = []
cv2.namedWindow('RGB image')
cv2.setMouseCallback('RGB image', get_position)

#function to get RGB image from kinect
def get_video():
    array,_ = freenect.sync_get_video()
    array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
    return array
 
#function to get depth image from kinect
def get_depth():
    global depth 
    depth, _ = freenect.sync_get_depth()
 
if __name__ == "__main__":
    #get a frame from RGB camera
    frame = get_video()

    cimg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(cimg,cv2.HOUGH_GRADIENT,1,20,param1=100,param2=100,minRadius=0,maxRadius=500)
    circles = np.uint16(np.around(circles))
    
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

    cv2.imshow('detected circles',cimg)
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