function [cLine,cPoly,cCir,cArc,cPoi,cSpline] = dxfToXY(dxfFilePath)
fId = fopen(dxfFilePath); %open the desired dxf file
data = textscan(fId,'%d%s','Delimiter','\n'); %read the whole file in form of key and value
fclose(fId); %close the file
groupCode = data{1}; %group codes saved in this variable
values = data{2}; %associated values with each code in this variable

%Finding 0 => SECTION , 2 => ENTITIES they are in sequence: 
%0
%SECTION
%2
%ENTITIES
possiblePos = find(groupCode==0); %SECTION Group Code = 0
mappedPosEntities = strmatch('ENTITIES', values(possiblePos(1:end-1)+1), 'exact'); %search fo ENTITIES only after 0 groupCodes neglecting 
                                                                                   %the last 0 as it is the end of file and +1 because ENTITIES comes
                                                                                   %after SECTION with group code 0.
                                                                                   
%Finding 0 => ENDSEC in sequence:
%0
%ENDSEC
mappedposEndSec = strmatch('ENDSEC',values(possiblePos(mappedPosEntities:end)),'exact'); 

possiblePos = possiblePos(mappedPosEntities:mappedPosEntities-1+mappedposEndSec(1));% Taking the first EndSec after Section Entities

cLine = cell(1,1);
cPoly = cell(1,1);
cCir = cell(1,1);
cArc = cell(1,1);
cPoi = cell(1,1);
cSpline = cell(1,1);
%
iLine = 1;
iPoly = 1;
iCir = 1;  
iArc = 1;
iPoi = 1;
iSpline = 1;

% Loop on the Entities
for iEnt = 1:length(possiblePos)-2
    groupCodeEnt = groupCode(possiblePos(iEnt+1):possiblePos(iEnt+2)-1); %get all group codes in the current entity  
    valuesEnt = values(possiblePos(iEnt+1):possiblePos(iEnt+2)-1); %get all values in the current entity
    current = valuesEnt{1}; 
    %In the entitie's name is assumed uppercase
    switch current            
        case 'LINE'
            % (Xi,Yi,Xj,Yj) start and end points
            xStart = str2double(f_ValGrCode(10,groupCodeEnt,valuesEnt));
            xEnd = str2double(f_ValGrCode(11,groupCodeEnt,valuesEnt));
            yStart = str2double(f_ValGrCode(20,groupCodeEnt,valuesEnt));
            yEnd = str2double(f_ValGrCode(21,groupCodeEnt,valuesEnt));
            cLine{iLine,1} = [xStart xEnd];
            cLine{iLine,2} = [yStart yEnd];
            iLine = iLine+1;  
        case 'LWPOLYLINE'%%%%%%
            % (X,Y) vertexs
            %%%Is not take into account the budge (group code 42, arc in the polyline).
            m_Coord = [str2double(f_ValGrCode(10,groupCodeEnt,valuesEnt)),...
                    str2double(f_ValGrCode(20,groupCodeEnt,valuesEnt))];
            if strcmp(f_ValGrCode(70,groupCodeEnt,valuesEnt),'1')&&...
                    any(m_Coord(1,:)~=m_Coord(end,:))
                %Close polyline
                cPoly{iPoly,1} = [m_Coord;m_Coord(1,:)];
            else
                cPoly{iPoly,1} = m_Coord;
            end
            iPoly = iPoly+1;   
        case 'CIRCLE'
            % (X Center,Y Center,Radius)
            xCenter = str2double(f_ValGrCode(10,groupCodeEnt,valuesEnt));
            yCenter = str2double(f_ValGrCode(20,groupCodeEnt,valuesEnt));
            radius = str2double(f_ValGrCode(40,groupCodeEnt,valuesEnt));
            cCir{iCir,1} = [ xCenter,yCenter,radius ];
            iCir = iCir+1;
        case 'ARC'%%%%%%%%
            % (X Center,Y Center,Radius,Start angle,End angle)
            cArc{iArc,1} = [str2double(f_ValGrCode(10,groupCodeEnt,valuesEnt)),...
                str2double(f_ValGrCode(20,groupCodeEnt,valuesEnt)),...
                str2double(f_ValGrCode(40,groupCodeEnt,valuesEnt)),...
                str2double(f_ValGrCode(50,groupCodeEnt,valuesEnt)),...
                str2double(f_ValGrCode(51,groupCodeEnt,valuesEnt))];
            iArc = iArc+1;
        case 'POINT'
            % (X,Y) Position
            cPoi{iPoi,1} = str2double(f_ValGrCode(10,groupCodeEnt,valuesEnt));
            cPoi{iPoi,1} = str2double(f_ValGrCode(20,groupCodeEnt,valuesEnt));
            iPoi = iPoi+1;
        case 'SPLINE'%%%%%%%%%%
            xVector = [];
            yVector = [];
            for i=1:length(groupCodeEnt)
               if(groupCodeEnt(i) == 10 )%|| groupCodeEnt(i) == 11) 
                xVector = [xVector str2double(valuesEnt(i))];
               elseif(groupCodeEnt(i) == 20) %|| groupCodeEnt(i) == 21)we only take nw control points no fit points
                yVector = [yVector str2double(valuesEnt(i))];
               end
            end
            cSpline{iSpline,1} = xVector;
            cSpline{iSpline,2} = yVector;
            iSpline = iSpline+1;
    end        
end 
end
%%   

function c_Val = f_ValGrCode(grCode,grCodes,vals)
    c_Val = vals(grCodes==grCode);
end


