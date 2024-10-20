%% This is the main execution file.
clc; clear; close all;

%% Subject IDs
subject_id = [46343, 759667, 781756, 844359, 1066528, 1360686, 1449548,...
    1455390, 1818471, 2598705, 2638030, 3509524, 3997827, 4018081, ...
    4314139, 4426783, 5132496, 5383425, 5498603, 5797046, 6220552, ...
    8000685, 8173033, 8258170, 8530312, 8686948, 8692923, ...
    9106476, 9618981, 9961348, 7749105];

% subject_id = [46343];

for i = 1:numel(subject_id)
    
    id = subject_id(i);

    %% Load the subject file to get the timezone -- This is to run data on WDAP
    fid = fopen('subject.txt');
    tline = fgetl(fid);
    sub_file = cell(0,1);
    while ischar(tline)
        sub_file{end+1,1} = tline;
        tline = fgetl(fid);
    end
    fclose(fid);
    timezone = sub_file{2};
    
    ref_date = datenum(1970,1,1);
    bin_size = 5;
    
    try
        if(isempty(timezone))
	    t_offset=0;
        else
    	    t_offset = tzoffset(datetime('today', 'TimeZone', timezone));
    	    t_offset = datenum(t_offset);
        end
    catch
        t_offset = 0;
    end
    
    try
        hr = readtable('TDA_Wearable_Sleep_Classifier/Raw_data/heart_rate/' + string(id) + '_heartrate.txt','Delimiter', ',');
        hr = table2array(hr(:,1:2));
        Thr = hr;
%         Thr(:,1) = Thr(:,1)/(24*60*60) + ref_date + t_offset;
    catch
        error('No heart rate file in directory.')
    end
    
    try
        steps1 = readtable('TDA_Wearable_Sleep_Classifier/Cropped_data/Steps/binned_steps/' + string(id) + '_binned_steps.txt', 'Delimiter', ',');
        steps2 = readtable('TDA_Wearable_Sleep_Classifier/Cropped_data/Steps/Preprocessed_steps/' + string(id) + '_preprocessed_steps.csv', 'Delimiter', ',');
        steps1 = table2array(steps1(:,1:2));
        steps2 = table2array(steps2(:,1:2));
        Tsteps1 = steps1;
        Tsteps2 = steps2;
        isEmptySteps = 0;
    catch
        Tsteps = [];
        isEmptySteps = 1;
    end

    Thr(:,1) = Thr(:,1)/(24*60*60);
    Tsteps = [Tsteps1((Tsteps1(:,1) < 0),:); Tsteps2((Tsteps2(:,1) >= 0),:)];
    Tsteps(:,1) = Tsteps(:,1)/(24*60*60);

    try
        Tsleep = readtable('TDA_Wearable_Sleep_Classifier/Raw_data/labels/' + string(id) + '_labeled_sleep.txt', 'Delimiter', ',');
        Tsleep = table2array(Tsleep(:,1:2));
        isEmptySleep = 0;
    catch
        Tsleep = [];
        isEmptySleep = 1;
    end 
    
    if(~isEmptySteps)
        %% Run Heart rate Algorithm
        [dmy_hr, heart_rate_proxy] = bayes_hr_estimator(Thr, Tsteps, bin_size, id);

    end

    csvwrite(strcat('TDA_Wearable_Sleep_Classifier/Features/Clock_proxies/CRHR', string(id),'_heart_rate_proxy.csv'), heart_rate_proxy);
end
