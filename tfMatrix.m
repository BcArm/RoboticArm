function Ai = tfMatrix(thi,ai,alphai,di)
%This function takes the parameters of the link and return its
%transformation matrix. 
%thetai and alphai in degrees.
x1 = [cos(thi*pi/180) -cos(alphai*pi/180)*sin(thi*pi/180) sin(alphai*pi/180)*sin(thi*pi/180) ai*cos(thi*pi/180)];
x2 = [sin(thi*pi/180) cos(alphai*pi/180)*cos(thi*pi/180) -sin(alphai*pi/180)*cos(thi*pi/180) ai*sin(thi*pi/180)];
x3 = [0 sin(alphai*pi/180) cos(alphai*pi/180) di];
x4 = [0 0 0 1];
Ai = [x1;x2;x3;x4];
end

