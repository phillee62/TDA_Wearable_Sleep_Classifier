function light_input = convert_steps_to_light(steps, stp_to_act)    
    
    light_input = zeros(numel(steps),1);
    activity = zeros(numel(steps),1);
    stp = stp_to_act;
    
    for i = 1:numel(steps)
        if isnan(steps(i))
            activity(i) = 0;
        else
            activity(i) = (30/stp)*steps(i);
        end
    end
    
    max_activity = max(activity)/2;
    
    for j = 1:numel(activity)
        if activity(j) <= 0
            light_input(j) = 0;
        elseif 0 < activity(j) && activity(j) < 0.1*max_activity
            light_input(j) = 100;
        elseif 0.1*max_activity <= activity(j) && activity(j) < 0.25*max_activity
            light_input(j) = 200;
        elseif 0.25*max_activity <= activity(j) && activity(j) <= 0.4*max_activity
            light_input(j) = 500;
        else
            light_input(j) = 2000;
        end
    end        
    
%     light_input = activity;
end