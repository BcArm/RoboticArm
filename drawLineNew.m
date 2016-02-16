function [] = drawLine( x0,y0,z0,x1,y1,z1,T,obj,divisions )
    syms x y z
    xflag = false;
    yflag = false;
    zflag = false;
    
    if((x1-x0)==0)
        xflag = true;
    end
    
    if((y1-y0)==0)
        yflag = true;
    end
    
    if((z1-z0)==0)
        zflag = true;
    end
    
    if(~xflag)
        eqn(1) = (x-x0)/(x1-x0);
    end
    
    if(~yflag)
        eqn(2) = (y-y0)/(y1-y0);
    end
    
    if(~zflag)
        eqn(3) = (z-z0)/(z1-z0);
    end 
    
    %check for the largest difference
    if(abs(x0-x1) >= abs(y0-y1))
        if(abs(x0-x1) >= abs(z0-z1))
            largest = 'x';
        else
            largest = 'z';
        end
    else
        if(abs(y0-y1) >= abs(z0-z1))
            largest = 'y';
        else
            largest = 'z';
        end
    end

    %calculate step
    if(largest == 'x')
        step = (x1-x0)/divisions;
    elseif(largest == 'y')
        step = (y1-y0)/divisions;
    else
        step = (z1-z0)/divisions;
    end

    %get the points on the line based on step
    for i=1:divisions+1
        if(largest == 'x')
            xVec(i) = x0 + step*(i-1);
            x = xVec(i);
            if(~yflag && ~zflag)
                [soly,solz]=solve(eqn(2)==subs(eqn(1)),eqn(3)==subs(eqn(1)));
                yVec(i) = soly;
                zVec(i) = solz;
            elseif(yflag && ~zflag)
                [solz]=solve(eqn(3)==subs(eqn(1)));
                yVec(i) = y0;
                zVec(i) = solz;
            elseif(~yflag && zflag)
                [soly]=solve(eqn(2)==subs(eqn(1)));
                yVec(i) = soly;
                zVec(i) = z0;
            else
                yVec(i) = y0;
                zVec(i) = z0;
            end
        elseif(largest == 'y')
            yVec(i) = y0 + step*(i-1);
            y = yVec(i);
            if(~xflag && ~zflag)
                [solx,solz]=solve(eqn(1)==subs(eqn(2)),eqn(3)==subs(eqn(2)));
                xVec(i) = solx;
                zVec(i) = solz;
            elseif(xflag && ~zflag)
                [solz]=solve(eqn(3)==subs(eqn(2)));
                xVec(i) = x0;
                zVec(i) = solz;
            elseif(~xflag && zflag)
                [solx]=solve(eqn(1)==subs(eqn(2)));
                xVec(i) = solx;
                zVec(i) = z0;
            else
                xVec(i) = x0;
                zVec(i) = z0;
            end
        else
            zVec(i) = z0 + step*(i-1);
            z = zVec(i);
            
            if(~xflag && ~yflag)
                [solx,soly]=solve(eqn(1)==subs(eqn(3)),eqn(2)==subs(eqn(3)));
                xVec(i) = solx;
                yVec(i) = soly;
            elseif(xflag && ~yflag)
                [soly]=solve(eqn(2)==subs(eqn(3)));
                xVec(i) = x0;
                yVec(i) = soly;
            elseif(~xflag && yflag)
                [solx]=solve(eqn(1)==subs(eqn(3)));
                xVec(i) = solx;
                yVec(i) = y0;
            else
                xVec(i) = x0;
                yVec(i) = y0;
            end
        end
    end
    
    %initial position
    s = invKinematics(double(xVec(1)),double(yVec(1)),double(zVec(1)),T,[0 0 0])
    th1(1) = s(1);
    th2(1) = s(2);
    th3(1) = s(3);
    th4(1) = s(4);
    th5(1) = s(5);

    %t = forwardKinematics(th1(1),th2(1),th3(1),th4(1),th5(1),T);
    
    %get theta vectors
    for i=2:divisions+1
        [double(xVec(i)) double(yVec(i)) double(zVec(i))]
        s = invKinematics(double(xVec(i)),double(yVec(i)),double(zVec(i)),T,[th2(i-1) th3(i-1) th4(i-1)])
        th1(i) = s(1);
        th2(i) = s(2);
        th3(i) = s(3);
        th4(i) = s(4);
        th5(i) = s(5);
    end
    'khalaaaaaaaaaaast'
    pause(5);
    %send number of points
     if divisions<10
     fwrite(obj,strcat('0','0',int2str(divisions+1)));   
     elseif divisions<100
      fwrite(obj,strcat('0',int2str(divisions+1)));  
    else
     fwrite(obj,int2str(divisions+1));
    end
    %move the arm on the path
     for i=1:divisions+1
%         t = forwardKinematics(th1(i),th2(i),th3(i),th4(i),th5(i),T);
%         xVecNew(i) = t(1,4);
%         yVecNew(i) = t(2,4);
%         zVecNew(i) = t(3,4);
        pause(0.1);
        duty = goToDegree(th1(i),th2(i),th3(i),th4(i),th5(i),0)
        fwrite(obj,duty(1:9));
        pause(0.01)
        fwrite(obj,duty(10:18));
     end
%      figure
%      plot(th1)
%      figure
%      plot(th2)
%      figure
%      plot(th3)
%      figure
%      plot(th4)
%      figure
%      set(gcf,'NumberTitle','off')
%      set(gcf,'Name',strcat('Both Lines')) 
%      plot3(xVecNew,yVecNew,zVecNew,xVec,yVec,zVec);
%      figure
%      set(gcf,'NumberTitle','off')
%      set(gcf,'Name',strcat('Original Line'))
%      plot3(xVec,yVec,zVec);
%      figure
%      set(gcf,'NumberTitle','off')
%      set(gcf,'Name',strcat('After Inverse'))
%      plot3(xVecNew,yVecNew,zVecNew);
end

