function [] = drawTriangle( x1,y1,z1,x2,y2,z2,x3,y3,z3,T,obj,divisions )
    [th1,th2,th3,th4,th5] = drawLineShapes( x1,y1,z1,x2,y2,z2,T,divisions );
    
    [m1,m2,m3,m4,m5] = drawLineShapes( x2,y2,z2,x3,y3,z3,T,divisions );
    th1 = [th1 m1];
    th2 = [th2 m2];
    th3 = [th3 m3];
    th4 = [th4 m4];
    th5 = [th5 m5];
    
    [n1,n2,n3,n4,n5] = drawLineShapes( x3,y3,z3,x1,y1,z1,T,divisions );
    th1 = [th1 n1];
    th2 = [th2 n2];
    th3 = [th3 n3];
    th4 = [th4 n4];
    th5 = [th5 n5];
    save('triangle.mat','th1','th2','th3','th4','th5')
    while(1)
        pause(7);
        %send number of points
        if 3*divisions < 10
         fwrite(obj,strcat('0','0',int2str(3*divisions+3)));   
        elseif 3*divisions<100
          fwrite(obj,strcat('0',int2str(3*divisions+3)));  
        else
         fwrite(obj,int2str(3*divisions+3));
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

