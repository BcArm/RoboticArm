function [] = MoveObj(x1,y1,z1,x2,y2,z2,T,obj)
GoToPos(x1,y1,z1,T,obj,510);
GoToPos(x1,y1,z1-4,T,obj,510);
GoToPos(x1,y1,z1-4,T,obj,390);
GoToPos(x1,y1,z1+4,T,obj,390);
%drawLineNew(x1,y1,z1+3,x2,y2,z2+3,T,obj,2,390)
GoToPos(x2,y2,z2+4,T,obj,390);
GoToPos(x2,y2,z2-4,T,obj,390);
GoToPos(x2,y2,z2-4,T,obj,510);
GoToPos(x2,y2,z2+4,T,obj,510);
end

