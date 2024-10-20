function [new_hr_times, new_hr_values] = constant_steps_filter2(hr_times, hr_values, steps_times, steps_values, M)

s_length = length(steps_times);

is_zero = 0;

starts = [];
ends = [];

% Find all segments of zeros

for i = 1:s_length
    
    if(~is_zero)
        
        if(~steps_values(i)) && (i < s_length)
            
            starts = [starts; steps_times(i)];
            
            is_zero = 1;
            
        end

        
    else
        
        if(~steps_values(i))
            
            if(i == s_length)
                ends = [ends; steps_times(end)];
            else
            
                continue;
                
            end
            
        else
            
            ends = [ends; steps_times(i-1)];
            
            is_zero = 0;
            
        end
        
    end
    
end

segment_lengths = (ends-starts)*1440;

v = find(segment_lengths>M);

remove_segments = [starts(v) ends(v)];

if(isempty(v))
    new_hr_times = hr_times;
    new_hr_values = hr_values;
    
else
    
    for i = 1:length(v)
        
        hr_values(hr_times>=remove_segments(i,1) & hr_times<=remove_segments(i,2)) = [];
        hr_times(hr_times>=remove_segments(i,1) & hr_times<=remove_segments(i,2)) = [];
        
    end
    
    new_hr_times = hr_times;
    new_hr_values = hr_values;
    
end


    
