import cv2

capture = cv2.VideoCapture()

capture.open(cv2.CAP_OPENNI)

while 1:
    capture.grab()
    ok, rgb = capture.retrieve(0, cv2.CAP_OPENNI_BGR_IMAGE)
    cv2.imshow('RGB Image', rgb);
    if cv2.waitKey(5) & 0xFF == 27:
        break;
cv2.destroyAllWindows()
