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
    
%     for i=1:size(th1,2)
%         pause(1);
%         duty = goToDegree(th1(i),th2(i),th3(i),th4(i),th5(i),0);
%         fwrite(obj,duty(1:9));
%         pause(0.01)
%         fwrite(obj,duty(10:18));
%     end
    
    while(1)
        pause(7);
        %send number of points
        if 4*divisions < 10
         fwrite(obj,strcat('0','0',int2str(4*divisions+4)));   
        elseif 4*divisions<100
          fwrite(obj,strcat('0',int2str(4*divisions+4)));  
        else
         fwrite(obj,int2str(4*divisions+4));
        end
        for i=1:size(th1,2)
            pause(0.1);
            duty = goToDegree(th1(i),th2(i),th3(i),th4(i),th5(i),0);
            fwrite(obj,duty(1:9));
            pause(0.01)
            fwrite(obj,duty(10:18));
        end
    end
end

