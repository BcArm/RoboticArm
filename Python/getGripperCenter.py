import cv2

def getGripperCenter(img):
    
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

    redImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    yelImg = redImg.copy()
    for i in xrange(img.shape[0]):
        for j in xrange(img.shape[1]):
            b, g, r = map(int, img[i, j])
            if (r - b > 30 and r - g > 30 and abs(g - b) < 30 and max(b, g) < 100):
                redImg[i, j] = 255
            else:
                redImg[i, j] = 0

    for i in xrange(img.shape[0]):
        for j in xrange(img.shape[1]):
            b, g, r = map(int, img[i, j])
            if (abs(r - g) < 30 and r - b > 30 and g - b > 30 and min(r, g) > 100):
                yelImg[i, j] = 255
            else:
                yelImg[i, j] = 0

    redImg = cv2.medianBlur(redImg, 5)
    yelImg = cv2.medianBlur(yelImg, 5)

    redImg = cv2.GaussianBlur(redImg, (9, 9), 0)
    yelImg = cv2.GaussianBlur(yelImg, (9, 9), 0)

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

    return result