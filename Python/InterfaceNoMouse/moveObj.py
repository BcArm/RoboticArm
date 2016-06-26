from goToPosition import GoToPos
import time
import serial

def moveObj(x0, y0, z0, x1, y1, z1):
	ser = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=3.0)
	
	GoToPos(x0,y0,(1.85*z0) + 4,'open')
	time.sleep(1.5)
	GoToPos(x0,y0,(1.1*z0),'open')
	time.sleep(1.5)
	GoToPos(x0,y0,(1.1*z0),'close')
	time.sleep(1.5)
	GoToPos(x0,y0,(1.85*z0) + 4,'close')
	time.sleep(1.5)

	GoToPos(x1,y1,(1.85*z1) + 4,'close')
	time.sleep(1.5)
	GoToPos(x1,y1,(1.1 *z1),'close')
	time.sleep(1.5)
	GoToPos(x1,y1,(1.1 *z1),'open')