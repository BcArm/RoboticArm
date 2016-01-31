function t=forwardKinematics(x1,x2,x3,x4,x5,T)
    x1=(x1+90)*pi/180;
    x2=x2*pi/180;
    x3=x3*pi/180;
    x4=(x4-90)*pi/180;
    x5=x5*pi/180;

    t=double(subs(T));
end