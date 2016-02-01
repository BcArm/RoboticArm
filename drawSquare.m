function [] = drawSquare( x1,y1,z1,x2,y2,z2,x3,y3,z3,x4,y4,z4,T,obj,divisions )
    [th1,th2,th3,th4,th5] = drawLineShapes( x1,y1,z1,x2,y2,z2,T,divisions );
    
    [m1,m2,m3,m4,m5] = drawLineShapes( x2,y2,z2,x3,y3,z3,T,divisions );
    th1 = [th1 m1];
    th2 = [th2 m2];
    th3 = [th3 m3];
    th4 = [th4 m4];
    th5 = [th5 m5];
    
    [n1,n2,n3,n4,n5] = drawLineShapes( x3,y3,z3,x4,y4,z4,T,divisions );
    th1 = [th1 n1];
    th2 = [th2 n2];
    th3 = [th3 n3];
    th4 = [th4 n4];
    th5 = [th5 n5];
    
    [w1,w2,w3,w4,w5] = drawLineShapes( x4,y4,z4,x1,y1,z1,T,divisions );
    th1 = [th1 w1];
    th2 = [th2 w2];
    th3 = [th3 w3];
    th4 = [th4 w4];
    th5 = [th5 w5];
    
    for i=1:size(th1,2)
        pause(1);
        fwrite(obj,goToDegree('1',th1(i)));
        pause(0.00001);
        fwrite(obj,goToDegree('2',th2(i)));
        pause(0.00001);
        fwrite(obj,goToDegree('6',th3(i)));%%%%%%%%%
        pause(0.00001);
        fwrite(obj,goToDegree('4',th4(i)));
        %pause(0.0001);
        %fwrite(obj,goToDegree('5',th5(i)));
        %pause(0.001);
    end
end

