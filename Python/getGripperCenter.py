import cv2
import numpy as np
'''def getGripperCenter(img):
    def onMouse(event, x, y, f, g):
        print("hsv" + str(hsvImg[y, x, :]))
        print("img" + str(img[y, x, :]))
    def getCentroids(img):
        nLabels, labels = cv2.connectedComponents(img, 8)
        X = [0] * nLabels
        Y = [0] * nLabels
        cnt = [0] * nLabels
        for r in xrange(img.shape[0]):
            for c in xrange(img.shape[1]):
                label = labels[r, c]
                X[label] += r
                Y[label] += c
                cnt[label] += 1
        ret = []
        for i in xrange(1, nLabels):
            if (cnt[i] > 50):
                ret.append((X[i] / cnt[i], Y[i] / cnt[i]))
        return ret

    def getDistance(X, Y):
        dx = X[0] - Y[0]
        dy = X[1] - Y[1]
        return dx * dx + dy * dy
##    img = cv2.resize(img, (600, 600))
    
##    alpha = 0.8
##    beta = 70
##    for x in range(img.shape[0]):
##        for y in range(img.shape[1]):
##            for c in range(3):
##                img[x, y, c] = img[x, y, c] * alpha + beta
##    cv2.imshow("Current", img)
    hsvImg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    lower_red_hue_range = cv2.inRange(hsvImg, (0, 100, 100), (10, 255, 255))
    upper_red_hue_range = cv2.inRange(hsvImg, (160, 100, 50), (185, 255, 255))
    red_hue_image = cv2.addWeighted(lower_red_hue_range, 1.0, upper_red_hue_range, 1.0, 0.0)
    redImg = red_hue_image.copy()
    
##    redImg = cv2.inRange(hsvImg, (165, 200, 30), (195, 255, 70))
##    yelImg = cv2.inRange(hsvImg, (0, 140, 90), (30, 255, 160))

    lower_yel_hue_range = cv2.inRange(img, (0, 120, 130), (100, 255, 255))
    upper_yel_hue_range = cv2.inRange(img, (0, 120, 130), (100, 255, 255))
    yel_hue_image = cv2.addWeighted(lower_yel_hue_range, 1.0, upper_yel_hue_range, 1.0, 0.0)
    yelImg = yel_hue_image.copy()
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            b, g, r = map(int, img[x, y, :])
            if (b <= 150 and r >= 100 and g >= 50 and abs(r - g) <= 60 and min(r, g) >= 1.7 * b):
                yelImg[x, y] = 255


    
    redImg = cv2.medianBlur(redImg, 5)
    yelImg = cv2.medianBlur(yelImg, 5)

    redImg = cv2.GaussianBlur(redImg, (9, 9), 0)
    yelImg = cv2.GaussianBlur(yelImg, (9, 9), 0)


##    cv2.imshow("RED", redImg)
##    cv2.imshow("YEL", yelImg)

    cenRed = getCentroids(redImg)
    cenYel = getCentroids(yelImg)

    minD = -1
    result = (0, 0)
    for a in cenRed:
        for b in cenYel:
            d = getDistance(a, b)
            if (minD < 0 or d < minD):
                minD = d
                result = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    out = img.copy()
    cv2.circle(out, (result[1], result[0]), 10, (0, 255, 0), 2)
    cv2.imshow("Output", out)
##    cv2.setMouseCallback("Current", onMouse, 0 );
    cv2.waitKey(0)
    return result
'''
mouseX = -1000 
mouseY = -1000
def get_xy(event,x,y,flags,param):
    global mouseX,mouseY
    if event == cv2.EVENT_LBUTTONDBLCLK:
        mouseX,mouseY = x,y

def getGripperCenter(img):
    global mouseX,mouseY
    cv2.namedWindow('mouse_img')
    cv2.setMouseCallback('mouse_img', get_xy)
    while(1):
        cv2.imshow('mouse_img',img)
        k = cv2.waitKey(20) & 0xFF
        if mouseX != -1000 and mouseY != -1000:
            X = mouseX
            Y = mouseY
            mouseX = -1000
            mouseY = -1000
            return [X,Y]
