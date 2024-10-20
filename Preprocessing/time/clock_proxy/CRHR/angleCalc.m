% This function computes the angle from sin and cos values (-180,180]
% degree.
% Usage: 
% theta=angleCalc(S,C,out_mode)
%
% S: sin value of the angle
% C: cos value of the angle
% out_mode: 'deg' OR 'rad'
% default output mode is in degree 
% the 
%
% Example:  
% theta= angleCalc(sin(-2*pi/3),cos(-2*pi/3))
% theta = -120;
% theta= angleCalc(sin(2*pi/3),cos(2*pi/3),'rad')
% theta= 2.0944  [rad]
%                            --------------Disi A Jun 25, 2013

function theta=angleCalc(S,C,out_mode)

if nargin<3
    out_mode='deg';
end

if strcmp(out_mode,'deg')
    cons=180/pi;
else
    cons=1;
end

theta=asin(S);
if C<0
    if S>0
        theta=pi-theta;
    elseif S<0
        theta=-pi-theta;
    else
        theta=theta+pi;
    end
end

theta=theta*cons;

end