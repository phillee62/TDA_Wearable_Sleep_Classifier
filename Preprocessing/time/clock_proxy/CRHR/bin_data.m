function [hr_data, steps_data] = bin_data(hr_data, steps_data, bin_size, num_day)
    %% Inputs:

    % 1. hr_data - a two column array, the first column lists the epoch
    % time date in days (e.g., 738157 is 01-Jan-2021), the second column lists
    % the heart rate value at that time
    % 2. steps_data - a two column array like the heart rate data, but the
    % second column is the steps value at the respective time
    % 3. bin_size - the number of minutes to bin the data (5 is suggested)

    %% Process data
    hr_dates = hr_data(:,1);
    steps_dates = steps_data(:,1);
    hr_vals = hr_data(:,2);
    steps_vals = steps_data(:,2);

    %% Save all the days in the interval of data given to loop over
    hr_days = floor(hr_dates);
    dmy_hr = unique(hr_days,'rows','stable');
    dmy_hr = (dmy_hr(1):dmy_hr(end)+1).';
    i = num_day;
    
    if num_day == 0
        start_time = (dmy_hr(1))*60*24;
        
        %% Remove hr_times and hr_values where steps are zero consecutively for more 2 hours would be correct
        [hr_dates, hr_vals] = constant_steps_filter2(hr_dates, hr_vals, steps_dates, steps_vals, 120);

        %% Load steps information for that day    
        steps_times = steps_dates(steps_dates>=dmy_hr(1) & steps_dates < dmy_hr(2));    
        steps_values = steps_vals(steps_dates>=dmy_hr(1) & steps_dates < dmy_hr(2));  

        %% Load heart rate data for the specific day
        hr_times = hr_dates(hr_dates < dmy_hr(2) & hr_dates >= dmy_hr(1));
        hr_values = hr_vals(hr_dates < dmy_hr(2) & hr_dates >= dmy_hr(1));
        
        %% Initialize the output array
        hr_data = zeros(24*60/bin_size,2);
        steps_data = zeros(24*60/bin_size,2);
        hr_data(:,1) = [bin_size:bin_size:24*60]';
        steps_data(:,1) = [bin_size:bin_size:24*60]';
    else
        start_time = dmy_hr(num_day+1)*60*24;
        
        %% Remove hr_times and hr_values where steps are zero consecutively for more 2 hours would be correct
        [hr_dates, hr_vals] = constant_steps_filter2(hr_dates, hr_vals, steps_dates, steps_vals, 120);

        %% Load steps information for that day    
% %         steps_times = steps_dates(steps_dates>=dmy_hr(i)+1 & steps_dates < dmy_hr(i)+2);    
% %         steps_values = steps_vals(steps_dates>=dmy_hr(i)+1 & steps_dates < dmy_hr(i)+2);  
        steps_times = steps_dates(steps_dates>=dmy_hr(i) & steps_dates < dmy_hr(i)+1);    
        steps_values = steps_vals(steps_dates>=dmy_hr(i) & steps_dates < dmy_hr(i)+1);  

        %% Load heart rate data for the specific day
%         hr_times = hr_dates(hr_dates < dmy_hr(i)+2 & hr_dates >= dmy_hr(i)+1);
%         hr_values = hr_vals(hr_dates < dmy_hr(i)+2 & hr_dates >= dmy_hr(i)+1);
        hr_times = hr_dates(hr_dates < dmy_hr(i)+1 & hr_dates >= dmy_hr(i));
        hr_values = hr_vals(hr_dates < dmy_hr(i)+1 & hr_dates >= dmy_hr(i));
        
        %% Initialize the output array
        hr_data = zeros(24*60/bin_size,2);
        steps_data = zeros(24*60/bin_size,2);
        hr_data(:,1) = [24*60*(num_day-1)+bin_size:bin_size:24*60*num_day]';
        steps_data(:,1) = [24*60*(num_day-1)+bin_size:bin_size:24*60*num_day]';
    end

    %% Check if steps data is empty (or <= 20 measurements)
    if numel(steps_times) <= 20
        steps_data = [];
        hr_data = [];
    else
        %% Convert the times data to minutes  
        hr_times = hr_times*24*60 - start_time;
        steps_times = steps_times*24*60 - start_time;
        raw_steps_data = [steps_times steps_values];
        raw_hr_data = [hr_times hr_values];

        %% Find all unique binned times for HR data
        [hr_avg, ~, idx_hr] = unique(floor(raw_hr_data(:,1)/bin_size), 'stable');

        %% Average HR measurements in same bin
        val_hr = accumarray(idx_hr, raw_hr_data(:, 2), [], @mean);

        %% Repeat the same for steps data
        [steps_avg, ~, idx_steps] = unique(floor(raw_steps_data(:,1)/bin_size), 'stable');
        val_steps = accumarray(idx_steps, raw_steps_data(:,2), [], @mean);
        steps_avg = steps_avg + 1;

        %% Fill in the Heart rate and Steps data for the given day
        for t = 1:24*60/bin_size
            try
                if ~isempty(find(t == hr_avg, 1))
                   hr_data(t,2) = val_hr(find(t == hr_avg,1));
                else
                   hr_data(t,2) = 0;
                end
            catch
                hr_data(t,2) = 0;
            end    
            try
                if ~isempty(find(t == steps_avg, 1))
                   steps_data(t,2) = val_steps(find(t == steps_avg,1));
                else
                   steps_data(t,2) = 0;
                end
            catch
                steps_data(t,2) = 0;
            end
        end
    end
end
