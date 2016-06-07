import time
import numpy
import serial
from sympy import *
from InvKin import  invKin 
from goToDegree import goToDegree
x, y, z = symbols('x y z')

x0 = -10
y0 = 25
z0 = 8.7

def DrawLineGoToPos(x1,y1,z1,gr,initial_guess,divisions):
    xflag = False
    yflag = False
    zflag = False

    if((x1-x0)==0):
        xflag = True

    if((y1-y0)==0):
        yflag = True

    if((z1-z0)==0):
        zflag = True

    if(not xflag):
        eqnX = (x-x0)/(x1-x0)

    if(not yflag):
        eqnY = (y-y0)/(y1-y0)

    if(not zflag):
        eqnZ = (z-z0)/(z1-z0)

    #check for the largest difference
    if(abs(x0-x1) >= abs(y0-y1)):
        if(abs(x0-x1) >= abs(z0-z1)):
            largest = 'x'
        else:
            largest = 'z'
    else:
        if(abs(y0-y1) >= abs(z0-z1)):
            largest = 'y'
        else:
            largest = 'z'

    #calculate step
    if(largest == 'x'):
        step = (x1-x0)/divisions
    elif(largest == 'y'):
        step = (y1-y0)/divisions
    else:
        step = (z1-z0)/divisions

    xVec = []
    yVec = []
    zVec = []

    for i in range (0,divisions+1):
        if(largest == 'x'):
            xVec.append(x0 + step*(i))
            xS = xVec[i]
            if(not yflag and not zflag):
                yVec.append(solve(eqnY-eqnX.subs(x,xS).evalf())[0])
                zVec.append(solve(eqnZ-eqnX.subs(x,xS).evalf())[0])
            elif(yflag and not zflag):
                yVec.append(y0)
                zVec.append(solve(eqnZ-eqnX.subs(x,xS).evalf())[0])
            elif(not yflag and zflag):
                zVec.append(z0)
                yVec.append(solve(eqnY-eqnX.subs(x,xS).evalf())[0])
            else:
                yVec.append(y0)
                zVec.append(z0)
        elif(largest == 'y'):
            yVec.append(y0 + step*(i))
            yS = yVec[i]
            if(not xflag and not zflag):
                xVec.append(solve(eqnX-eqnY.subs(y,yS).evalf())[0])
                zVec.append(solve(eqnZ-eqnY.subs(y,yS).evalf())[0])
            elif(xflag and not zflag):
                xVec.append(x0)
                zVec.append(solve(eqnZ-eqnY.subs(y,yS).evalf())[0])
            elif(not xflag and zflag):
                zVec.append(z0)
                xVec.append(solve(eqnX-eqnY.subs(y,yS).evalf())[0])
            else:
                xVec.append(x0)
                zVec.append(z0)
        else:
            zVec.append(z0 + step*(i))
            zS = zVec[i]
            if(not xflag and not yflag):
                xVec.append(solve(eqnX-eqnZ.subs(z,zS).evalf())[0])
                yVec.append(solve(eqnY-eqnZ.subs(z,zS).evalf())[0])
            elif(xflag and not yflag):
                xVec.append(x0)
                yVec.append(solve(eqnY-eqnZ.subs(z,zS).evalf())[0])
            elif(not xflag and yflag):
                yVec.append(y0)
                xVec.append(solve(eqnX-eqnZ.subs(z,zS).evalf())[0])
            else:
                xVec.append(x0)
                yVec.append(y0)
    print xVec
    print yVec
    print zVec


    th1 = []
    th2 = []
    th3 = []
    th4 = []
    th5 = []

    for i in (1:divisions+1):
        s = invKinematics(xVec(i),yVec(i),zVec(i),[th2(i-1),th3(i-1),th4(i-1)])
        th1.append(s[0])
        th2.append(s[1])
        th3.append(s[2])
        th4.append(s[3])
        th5.append(s[4])

    ser.write(str(0)+str(0)+str(1))

    for i in (0,divisions+1):
        duty = goToDegree(th1[i],th2[i]+8,th3[i],th4[i],th5[i],gr)
        print(duty)
        time.sleep(0.1)
        ser.write(duty[0:9])
        time.sleep(0.01)
        ser.write(duty[9:18])

DrawLineGoToPos(10,25,8.7,'open',[0,0,0],10)


