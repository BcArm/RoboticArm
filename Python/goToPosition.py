import time
import numpy
import serial
from InvKin import  invKin 
from goToDegree import goToDegree
def GoToPos( x,y,z,gr ):
    #check the baud rate, change the com port depending on the com, linux has another format ex.: '/dev/tty.usbserial'
    ser = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=3.0)
    s = invKin(x,y,z,[111.628,70.866,-65.91])
    print(s)
    #if the upcoming line is not working; try this:ser.write(b'obj,'0'+'0'+str(1)')
    duty = goToDegree(s[0],s[1]+8,s[2],s[3],s[4],gr)
    #duty = '364379490123348508'
    print(duty)
    ser.write(str(0)+str(0)+str(1))
    time.sleep(0.1)
    #use hint in the above comment if needed
    ser.write(duty[0:9])
    time.sleep(0.01)
    #use hint in the above comment if needed
    ser.write(duty[9:18])


#GoToPos(-13.583214977050545, 25.125725605442064, 1.0141989694782554,'open')
#GoToPos(0,21.22,15,'open')
#GoToPos(3,18,5,'close')
#GoToPos(10,21,15,'open')