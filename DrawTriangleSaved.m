function [] = DrawTriangleSaved(obj)
    while(1)
        pause(7);
        load('triangle.mat')
        %send number of points
        fwrite(obj,strcat('0',int2str(18)));
        for i=1:size(th1,2)
            pause(0.1);
            duty = goToDegree(th1(i),th2(i),th3(i),th4(i),th5(i),450);
            fwrite(obj,duty(1:9));
            pause(0.01)
            fwrite(obj,duty(10:18));
        end
    end
end

