function [] = GoToPos( x,y,z,T,obj,gr )
    s = invKinematics(x,y,z,T,[0 0 0])
    fwrite(obj,strcat('0','0',int2str(1)));
    pause(0.1);
    duty = goToDegree(s(1),s(2),s(3),s(4),s(5),'open')
    fwrite(obj,duty(1:9));
    pause(0.01)
    fwrite(obj,strcat(duty(10:18)));
end

