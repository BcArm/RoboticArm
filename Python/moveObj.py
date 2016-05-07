from goToPosition import GoToPos
import time
def moveObj(x,y,z):
	GoToPos(x,y,z+4,'open')
	print(x,y,z+4)
	time.sleep(1)
	GoToPos(x,y,z-4,'open')
	print(x,y,z-4)
	time.sleep(1)
	GoToPos(x,y,z-4,'close')
	print(x,y,z-4)
	time.sleep(1)
	GoToPos(x,y,z+4,'close')
	print(x,y,z+4)


	