import time
import serial

ser = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=3.0)


ser.write(str(0)+str(0)+str(1))
time.sleep(0.1)
ser.write('404399500')
time.sleep(0.01)
ser.write('230348552')
