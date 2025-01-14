import numpy as np
import pandas as pd
from .Topological_features import Load_motion, Load_hr, Load_sleep, Interpolate_data, Get_epoch_data
from .Topological_features import Find_embedding_params, Motion_TFs, HR_TFs
from gtda.time_series import SingleTakensEmbedding

def Extract_TFs(subject_ID: str):
  ##### Load preprocessed data for each subject #####
  motion = Load_motion(subject_ID)
  hr = Load_hr(subject_ID)
  sleep = Load_sleep(subject_ID)

  mot_TDA1 = []; mot_TDA0 = []
  hr_TDA1 = []; hr_TDA0 = []
  psg = []; time = []

  ##### Determine the total number of 30-sec epochs, interpolation and window size parameters #####
  numEpoch = len(sleep)-1
  interp_intv = 1
  # interp_intv = 2
  window_size = 210
  # window_size = 90
  num_nearby_epoch = int((window_size-30)/(2*30))

  ##### Interpolate motion and heart rate data for each subject #####
  motion_new, heart_rate = Interpolate_data(motion, hr, sleep, numEpoch, interp_intv, window_size)
  # motion_new = motion_new['norm']

  ##### Choose delay embedding parameters #####
  motion_embed_param, hr_embed_param = Find_embedding_params(motion_new['norm'], heart_rate['heart rate'], interp_intv, num_nearby_epoch)

  for j in range(0,numEpoch+1):
    ##### Extract data for each 30-sec epoch #####
    motion_epoch, hr_epoch, sleep_epoch = Get_epoch_data(motion_new, heart_rate, sleep, numEpoch, interp_intv, window_size, j)

    if sleep_epoch['sleep stage'].iloc[0] != -1 and not motion_epoch.empty:
      ##### Save PSG score & time stamp #####
      psg.append(sleep_epoch['sleep stage'].iloc[0])
      time.append(sleep_epoch['time'].iloc[0])

      ##### Proceed only when there are sufficiently many data point #####
      if motion_epoch.shape[0] <= 5:
        mot_TDA1.append(np.nan); mot_TDA0.append(np.nan)
        hr_TDA1.append(np.nan); hr_TDA0.append(np.nan)
      else:

        ##### Embed hr and motion data #####
        motion_STE = SingleTakensEmbedding(parameters_type='fixed', 
                                          dimension=motion_embed_param[0], 
                                          time_delay=motion_embed_param[1], 
                                          n_jobs=-1)

        motion_embed = motion_STE.fit_transform(motion_epoch['norm'])

        hr_STE = SingleTakensEmbedding(parameters_type='fixed', 
                                      dimension=hr_embed_param[0], 
                                      time_delay=hr_embed_param[1], 
                                      n_jobs=-1)

        hr_embed = hr_STE.fit_transform(hr_epoch['heart rate'])

        ##### Compute persistence diagram for motion data #####
        mot_H0_TF, mot_H1_TF = Motion_TFs(motion_embed)
        hr_H0_TF, hr_H1_TF = HR_TFs(hr_embed)

        mot_TDA0.append(mot_H0_TF); mot_TDA1.append(mot_H1_TF)
        hr_TDA0.append(hr_H0_TF); hr_TDA1.append(hr_H1_TF)

  print('Subject ID ' + str(subject_ID) + ' TFs extracted')

  TDA_feature_vec = pd.DataFrame()
  TDA_feature_vec['time'] = time
  TDA_feature_vec['motion H0'] = mot_TDA0
  TDA_feature_vec['motion H1'] = mot_TDA1
  TDA_feature_vec['heart rate H0'] = hr_TDA0
  TDA_feature_vec['heart rate H1'] = hr_TDA1
  TDA_feature_vec['psg'] = psg

  ##### Save TDA feature vector #####
  output_file = 'Features/Topological_features/' + str(subject_ID) + '_TFs.csv'
  TDA_feature_vec.to_csv(output_file, index=None)