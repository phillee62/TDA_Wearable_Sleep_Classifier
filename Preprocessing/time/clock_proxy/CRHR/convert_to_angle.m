function ang = convert_to_angle(y)
    
    x = y(1);
    xc = y(2);
    
    if x > 0 && xc > 0
        ang = 2*pi-atan2(xc,x);
    elseif x > 0 && xc <= 0 
        ang = -atan2(xc,x);
    elseif x < 0 && xc <= 0
        ang = -atan2(xc,x);
    elseif x < 0 && xc >= 0
        ang = 2*pi-atan2(xc,x);
    elseif x > 0 && xc == 0
        ang = 0;
    end
    
end