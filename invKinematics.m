function output = invKinematics(x,y,Z,T,g)
    th5=0;
    th1 = atand(abs(y)/abs(x));
    if(y==0&&x==0)
        th1=0;
    end
    if( y/x < 0 )
        th1 = 180 - th1;
    end
    theta1 = th1*pi/180;
    th5 = th5*pi/180;

    TOL=1e-10; %tolerance for imaginary check
    output = [1 2 3 4 5 0];
    g(3)=g(3)-90; %convert theta4 from arm angle to DH frame angle
    guess = g;
    sApproach = 1.05;%slope of approach vector
    flag=0; %flag for error accpetance
    options = optimoptions('fsolve','FunValCheck','off','Display','off');

    function fcns = eqns(z)  
        th2 = z(1); th3 = z(2); th4 = z(3);
        fcns(1) = cosd(th2-th3+th4) - sApproach;
        fcns(2) = 4*sind(th1)*( 2*cosd(th2 - th3) - 5*sind(th2 - th3 + th4) + 2*cosd(th2) )-y; 
        fcns(3) = 8*sind(th2 - th3) + 20*cosd(th2 - th3 + th4) + 8*sind(th2) + (31/5)-Z;
    end

    function [info,f] = solve
        [result,~,info] = fsolve(@eqns,guess,options);
        th2 = result(1)*pi/180;
        th3 = result(2)*pi/180;
        th4 = result(3)*pi/180;
        f = abs(imag(th2))<TOL&&abs(imag(th3))<TOL&&abs(imag(th4)<TOL); %imagenary check
    end

    function check 
        %function compares the position vector of the computed angles with 
        %the desired position vector and check if it's within accepted error
        x1 = th1*pi/180;
        x2 = th2;
        x3 = th3;
        x4 = th4;
        x5 = th5;
        e1 = double(subs(T));
        e1 = e1(1:4,4);
        e2 = [x;y;Z;1];
        e = abs(e2-e1);
        if(e<0.5)
            flag=1;
        else
            flag=0;
        end
    end

    for i= 1:41
        sApproach=sApproach-0.05;
        solve;
        check;
        
        if (flag)
            theta1 = th1-90;
            th2 = rad2deg(th2);
            th3 = rad2deg(th3);
            th4 = rad2deg(th4)+90;
            if( (theta1 <= 90) && (theta1 >= -85) )
               if((th2 <= 181) && (th2 >= -7))
                   if((th3 <= 81) && (th3 >= -102))
                       if((th4 <= 86) && (th4 >= -97))
                           output=[output;theta1,th2,th3,th4,th5,sApproach]; 
                       end
                   end
               end
            end 
        end
    end
    
    if(~flag)
        disp('error angles not found');
    end
    if( size(output,1) > 2 )
        prevThetas = [theta1 g(1) g(2) g(3)+90];
        nearest = output(2,:);
        diff1 = (prevThetas(1) - nearest(1))^2;
        diff2 = (prevThetas(2) - nearest(2))^2;
        diff3 = (prevThetas(3) - nearest(3))^2;
        diff4 = (prevThetas(4) - nearest(4))^2;
        D = diff1 + diff2 + diff3 + diff4;
        D = sqrt(D);
        minD = D;  
        for i = 3:size(output,1)
            current = output(i,:);
            diff1 = (prevThetas(1) - current(1))^2;
            diff2 = (prevThetas(2) - current(2))^2;
            diff3 = (prevThetas(3) - current(3))^2;
            diff4 = (prevThetas(4) - current(4))^2;
            D = diff1 + diff2 + diff3 + diff4;
            D = sqrt(D);
            if( D < minD )
                minD = D;
                nearest = current;
            end
        end
        output = nearest;
    elseif(size(output,1) == 2)
        output = output(2,:);
    else
        'mfeeeeeeeeeeeeeeesh 7all'
    end
end