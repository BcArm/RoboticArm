#import the necessary modules
import freenect
import cv2
import numpy as np
import math
from goToPosition import GoToPos

'''flag = 0
dif = np.array([0,0,0])'''
def get_position(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        '''global flag
        flag = (flag + 1) % 2'''
        zw = 1 / ( ( (depth[y][x])*-0.0030711016 )+ 3.3309495161 )
        zw = 100 * zw
        fx = 640 / (2 * math.tan(math.radians(57 / 2)))
        xw = zw * (x - 319) / fx
        fy = 480 / (2 * math.tan(math.radians(43 / 2)))
        yw = zw * (y - 239) / fy
        print xw,yw, zw
        print zw - 52, xw + 30, -(yw - 0.5) + 6.7
        GoToPos(-(zw - 52), xw + 30, -(yw - 0.5) + 6.7, 'open')
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
    while 1:
        #get a frame from RGB camera
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
