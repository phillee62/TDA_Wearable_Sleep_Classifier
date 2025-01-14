# import utils

class Constants(object):
    # WAKE_THRESHOLD = 0.3  # These values were used for scikit-learn 0.20.3, See:
    # REM_THRESHOLD = 0.35  # https://scikit-learn.org/stable/whats_new.html#version-0-21-0

    INCLUDE_CIRCADIAN = True
    EPOCH_DURATION_IN_SECONDS = 30
    SECONDS_PER_MINUTE = 60
    SECONDS_PER_DAY = 3600 * 24
    SECONDS_PER_HOUR = 3600
    VERBOSE = True

    CROPPED_FILE_PATH = 'Cropped_files/' # Make sure your current directory is "TDA_Wearable_Sleep_Classifier" 
    FEATURE_FILE_PATH = 'Features/'

    LOWER_BOUND = -0.2
    MATLAB_PATH = '/Applications/MATLAB_R2023b.app/bin/matlab'  # Replace with your MATLAB path
