import numpy as np
import pandas as pd
import scipy
import gtda
import ripser
import persim
from ripser import ripser
from persim import plot_diagrams

from scipy.interpolate import CubicSpline
from gtda.time_series import takens_embedding_optimal_parameters
from gtda.time_series import SingleTakensEmbedding
from gtda.time_series import TakensEmbedding
from gtda.time_series import Resampler
from persim.persistent_entropy import *

import warnings
warnings.filterwarnings("ignore")

def Load_motion(id):
  # df = pd.read_csv('Preprocessed_data/' + str(id) + '_cleaned_motion.out', header = None)
  df = pd.read_csv('Raw_data/' + str(i) + '_acceleration.txt', header = None)
  df_copy = df[0]
  t = []
  x = []
  y = []
  z = []

  for ii in range(0,len(df)):
    mot = df_copy[ii]
    idx1 = mot.find(" ")
    idx2 = mot.find(" ", idx1+1)
    idx3 = mot.find(" ", idx2+1)
    idx4 = len(mot)

    time = mot[0:idx1]
    x_mot = mot[idx1+1:idx2]
    y_mot = mot[idx2+1:idx3]
    z_mot = mot[idx3+1:idx4]

    t.append(float(time))
    x.append(float(x_mot))
    y.append(float(y_mot))
    z.append(float(z_mot))

  motion = pd.DataFrame()
  motion['time'] = t
  motion['x motion'] = x
  motion['y motion'] = y
  motion['z motion'] = z

  return motion

def Load_step(id):
  df = pd.read_csv('Preprocessed_data/' + str(id) + '_cleaned_counts.out', header = None)
  # df = pd.read_csv('Raw_data/' + str(id) + '_acceleration.txt', header = None)

  steps = pd.DataFrame()
  steps['time'] = df[0]
  steps['step counts'] = df[1]

  return steps

def Load_hr(id):
  df = pd.read_csv('Preprocessed_data/' + str(id) + '_cleaned_hr.out', header = None)
  df_copy = df[0]
  t = []
  hr = []

  for i_hr in range(0,len(df)):
    HR = df_copy[i_hr]

    idx1 = HR.find(" ")
    idx2 = len(HR)

    time = HR[0:idx1]
    hRate = HR[idx1+1:idx2]

    t.append(float(time))
    hr.append(float(hRate))

  heart_rate = pd.DataFrame()
  heart_rate['time'] = t
  heart_rate['heart rate'] = hr

  return heart_rate

def Load_sleep(id):
  df = pd.read_csv('Preprocessed_data/' + str(id) + '_cleaned_psg.out', header = None)
  df_copy = df[0]
  t = []
  psg = []

  for i_slp in range(0,len(df)):
    slp = df_copy[i_slp]

    idx1 = slp.find(" ")
    idx2 = len(slp)

    time = slp[0:idx1]
    slp_psg = slp[idx1+1:idx2]

    t.append(float(time))
    psg.append(float(slp_psg))

  sleep = pd.DataFrame()
  sleep['time'] = t
  sleep['sleep stage'] = psg

  return sleep

def Find_embedding_params(motion_Resampled: pd.DataFrame,
                          hr: pd.DataFrame,
                          sleep: pd.DataFrame,
                          numEpoch: float,
                          interp_intv: int,
                          window_size: int):

  num_nearby_epoch = int((window_size-30)/(2*30))
  max_param1 = 12
  max_param2 = int(((num_nearby_epoch+1)*30)/max_param1)

  ##### Interpolate heart rate data for each subject #####
  tspan = np.arange(0,int(sleep.iloc[numEpoch,0]+30), interp_intv)
  hr_CubicSpline = CubicSpline(hr['time'], hr['heart rate'])
  hr_interpolate = hr_CubicSpline(tspan)
  heart_rate = pd.DataFrame()
  heart_rate['time'] = tspan
  heart_rate['heart rate'] = hr_interpolate - np.mean(hr_interpolate)
  hr_interpolate_orig = hr_CubicSpline(tspan)
  hr_interpolate_orig-np.mean(hr_interpolate_orig)

  motion_embed_param = takens_embedding_optimal_parameters(motion_Resampled, max_param1, max_param2)
  hr_embed_param = takens_embedding_optimal_parameters(hr_interpolate_orig, max_param1, max_param2)

  return motion_embed_param, hr_embed_param

def Motion_TFs(motion_embed: np.array):
  ##### Compute persistence diagram for motion data #####
  dgm_mot0 = ripser(motion_embed)['dgms'][0]
  dgm_mot0 = np.array(dgm_mot0)

  dgm_mot1 = ripser(motion_embed)['dgms'][1]
  dgm_mot1 = np.array(dgm_mot1)

  if dgm_mot0.size == 0:
    mot_H0_TF = 0
  else:
    mot_persist0 = dgm_mot0[:,1] - dgm_mot0[:,0]
    try:
      mot_H0_TF = np.nanmax(mot_persist0[mot_persist0 != np.inf])
    except:
      mot_H0_TF = 0

  if dgm_mot1.size == 0:
    mot_H1_TF = 0
  else:
    mot_persist1 = dgm_mot1[:,1] - dgm_mot1[:,0]
    mot_H1_TF = np.max(mot_persist1)

  return mot_H0_TF, mot_H1_TF

def HR_TFs(hr_embed: np.array):
  ##### Compute persistence diagram for hr data #####
  dgm_hr0 = ripser(hr_embed)['dgms'][0]
  dgm_hr0 = np.array(dgm_hr0)

  dgm_hr1 = ripser(hr_embed)['dgms'][1]
  dgm_hr1 = np.array(dgm_hr1)
  hr_persist0 = dgm_hr0[:,1] - dgm_hr0[:,0]

  try:
    hr_H0_TF = np.nanmax(hr_persist0[hr_persist0 != np.inf])
  except:
    hr_H0_TF = 0

  if dgm_hr1.size == 0:
    hr_H1_TF = 0
  else:
    hr_persist1 = dgm_hr1[:,1] - dgm_hr1[:,0]
    hr_H1_TF = np.max(hr_persist1)

  return hr_H0_TF, hr_H1_TF

def Interpolate_data(motion: pd.DataFrame, hr: pd.DataFrame, sleep: pd.DataFrame, numEpoch: int):
  motion_CubicSpline = CubicSpline(motion['time'], motion.iloc[:,1:4])
  tspan = np.arange(0,int(sleep.iloc[numEpoch,0]+30), 1)

  motion_interpolate = motion_CubicSpline(tspan)
  motion_new = pd.DataFrame()
  motion_new['time'] = tspan
  motion_new['x motion'] = motion_interpolate[:,0]
  motion_new['y motion'] = motion_interpolate[:,1]
  motion_new['z motion'] = motion_interpolate[:,2]
  motion_new['norm'] =  np.linalg.norm(motion_interpolate[:,0:3], axis=1)

  ##### Interpolate heart rate data for each subject #####
  hr_CubicSpline = CubicSpline(hr['time'], hr['heart rate'])
  tspan = np.arange(0,int(sleep.iloc[numEpoch,0]+30), 1)
  hr_interpolate = hr_CubicSpline(tspan)
  heart_rate = pd.DataFrame()
  heart_rate['time'] = tspan
  heart_rate['heart rate'] = hr_interpolate - np.mean(hr_interpolate)

  return motion_new, heart_rate

def Get_epoch_data(motion_new: pd.DataFrame, heart_rate: pd.DataFrame, sleep: pd.DataFrame, numEpoch: int, j: int):
  sleep_epoch = sleep[(j*30 <= sleep.iloc[:,0]) & (sleep.iloc[:,0] < (j+1)*30)]

  if j < 3:
    motion_epoch = motion_new[(0 <= motion_new.iloc[:,0]) & (motion_new.iloc[:,0] < (j+4)*30)]
    hr_epoch = heart_rate[(0 <= heart_rate.iloc[:,0]) & (heart_rate.iloc[:,0] < (j+4)*30)]
  elif j > numEpoch-3:
    motion_epoch = motion_new[((j-3)*30 <= motion_new.iloc[:,0]) & (motion_new.iloc[:,0] < (numEpoch+1)*30)]
    hr_epoch = heart_rate[((j-3)*30 <= heart_rate.iloc[:,0]) & (heart_rate.iloc[:,0] < (numEpoch+1)*30)]
  else:
    motion_epoch = motion_new[((j-3)*30 <= motion_new.iloc[:,0]) & (motion_new.iloc[:,0] < (j+4)*30)]
    hr_epoch = heart_rate[((j-3)*30 <= heart_rate.iloc[:,0]) & (heart_rate.iloc[:,0] < (j+4)*30)]

  return motion_epoch, hr_epoch, sleep_epoch
