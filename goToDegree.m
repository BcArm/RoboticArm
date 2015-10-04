function y = goToDegree(motorNo,degree)
%This function takes motor number and degree for all servos and mapps it into
%the range for each motor
    if ( motorNo == '1' )
            value = (133/45)*degree + 364 ;
            if( value > 630 )
                value = 630 ;
            elseif( value < 110 )
                value = 110 ;
            end
    elseif ( motorNo == '2' )
            value = (258/90)*degree + 130 ;
            if( value > 650 )
                value = 650 ;
            elseif( value < 110 )
                value = 110 ;
            end
    elseif ( motorNo == '3' )
            value = (127/45)*degree + 400 ;
            if( value > 630 )
                value = 630 ;
            elseif( value < 110 )
                value = 110 ;
            end
    elseif ( motorNo == '4' )
            value = (127/45)*degree + 386 ;
            if( value > 630 )
                value = 630 ;
            elseif( value < 110 )
                value = 110 ;
            end
    elseif ( motorNo == '5' )
            if( strcmp(degree,'horizontal') )
                value = 590 ; 
            else
                value = 348 ;
            end
    elseif ( motorNo == '6' )
            if( strcmp(degree,'open') )
                value = 490 ;
            else
                value = 280 ;
    
            end
    end
     
    value = round(value);
    value = int2str(value);
    y = strcat(motorNo,value);
end

