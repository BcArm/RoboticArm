import math
import numpy as np

def goToDegree(deg1,deg2,deg3,deg4,deg5,deg6):

    value1 = (53.0/18.0)*deg1 + 110 
    if( value1 > 640 ):
        value1 = 640 
    elif( value1 < 110 ):
        value1 = 110 

    value2 = (17.0/6.0)*deg2 + 130 
    if( value2 > 640 ):
        value2 = 640 
    elif( value2 < 130 ):
        value2 = 130 
    
    value3 = (108.0/37.0)*deg3 + (4564.0/37.0)
    if( value3 > 640 ):
        value3 = 640 
    elif( value3 < 100 ):
        value3 = 100 
    
    value4 = (107.0/36.0)*deg4 + 100 
    if( value4 > 635 ):
        value4 = 635 
    elif( value4 < 100 ):
        value4 = 100 

    if( deg5 == 'horizontal' ):
        value5 = 580  
    else:
        value5 = 135 

    if( deg6 == 'open' ):
        value6 = 530 
    else:
        value6 = 130 

    value1 = int(round(value1))
    value2 = int(round(value2))
    value3 = int(round(value3))
    value4 = int(round(value4))
    value5 = int(round(value5))
    value6 = int(round(value6))
    value1 = str(value1)
    value2 = str(value2)
    value3 = str(value3)
    value4 = str(value4)
    value5 = str(value5)
    value6 = str(value6)
    
    return value1 + value2 + value6 + value4 + value5 + value3

