import math
import numpy as np

def goToDegree(deg1,deg2,deg3,deg4,deg5,deg6):

    value1 = (133/45)*deg1 + 364 
    if( value1 > 630 ):
        value1 = 630 
    elif( value1 < 110 ):
        value1 = 110 

    value2 = (258/90)*deg2 + 130 ;
    if( value2 > 650 ):
        value2 = 650 
    elif( value2 < 110 ):
        value2 = 110 
    
    value3 = (127/45)*deg3 + 400 
    if( value3 > 630 ):
        value3 = 630 
    elif( value3 < 110 ):
        value3 = 110 
    
    value4 = (127/45)*deg4 + 386 
    if( value4 > 630 ):
        value4 = 630 
    elif( value4 < 110 ):
        value4 = 110 

    if( deg5 == 'horizontal' ):
        value5 = 590  
    else:
        value5 = 348 

    if( deg6 == 'open' ):
        value6 = 490 
    else:
        value6 = 280 

    value1 = round(value1)
    value2 = round(value2)
    value3 = round(value3)
    value4 = round(value4)
    value5 = round(value5)
    value6 = round(value6)
    value1 = str(value1)
    value2 = str(value2)
    value3 = str(value3)
    value4 = str(value4)
    value5 = str(value5)
    value6 = str(value6)
    
    return value1 + value2 + value6 + value4 + value5 + value3
