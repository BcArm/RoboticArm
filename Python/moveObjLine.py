from goToPosDrawLine import DrawLineGoToPos
import time
import serial

def moveObjLine(x0,y0,z0,x1,y1,z1):
	ser = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=3.0)
	#grap object
	R = DrawLineGoToPos(0,21.22,12.86,x0,y0,z0+4,'open',[111.628,70.866,-65.91],10)
	time.sleep(1.5)
	R = DrawLineGoToPos(x0,y0,z0+4,x0,y0,z0-4,'open',R['guess'],3)
	time.sleep(1.5)
	#close
	ser.write(str(0)+str(0)+str(1))
	time.sleep(0.1)
	ser.write(R['angles'][0:6]+'390')
	time.sleep(0.1)
	ser.write(R['angles'][9:18])
	time.sleep(1.5)
	R = DrawLineGoToPos(x0,y0,z0-4,x0,y0,z0+4,'close',R['guess'],3)
	#place object in the desired position
	time.sleep(1.5)
	R = DrawLineGoToPos(x0,y0,z0+4,x1,y1,z1+4,'close',R['guess'],10)
	time.sleep(1.5)
	R = DrawLineGoToPos(x1,y1,z1+4,x1,y1,z1-4,'close',R['guess'],3)
	time.sleep(1.5)
	#open
	R = DrawLineGoToPos(x1,y1,z1-4,x1,y1,z1+4,'open',R['guess'],3)
	'''ser.write(str(0)+str(0)+str(1))
	time.sleep(0.1)
	ser.write(R['angles'][0:6]+'520')
	time.sleep(0.01)
	ser.write(R['angles'][9:18])'''

moveObjLine(0,30,8.7,-10,25,8.7)