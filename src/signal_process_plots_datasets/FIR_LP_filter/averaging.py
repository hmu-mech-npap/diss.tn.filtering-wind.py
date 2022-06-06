#%% [markdown]
# the aim of this file is to investigate the effect of the 
# averaging over decimated and filtered data.
# 
# i.e.: if the signal is recorded at f_r = 100 Hz by averaging all the data over 
#     $dt_r = \frac{1} {f_r}$ period would there be any observable differences for the 
#     a signal obtained at 100 kHZ, 50 KHz or 5 kHz? 
# 
#   Also, will filtering have an effect?
#
# so the idea is:
# - record a signal at a high rate (e.g. 100kHz)
# - For each decimation factor, decimate  the signal as required:
#       - apply a filter on the signal  (if required)
#       - split into  time periods of $dt_r$ duration and average the data
#       - Then at the end perform a power spectrum calculation 
# - plot the power spectrums with different decimation factors
# 
#%%
from pathlib import Path
from tkinter import N
from matplotlib import pyplot as plt
import scipy.signal as signal
import numpy as np
import pandas as pd

import nptdms
from nptdms import TdmsFile

from functions import spect,  plot_spect_comb2, Graph_data_container
from WT_NoiProc import WT_NoiseChannelProc, filter_Butter_default

import logging
logging.basicConfig( level=logging.WARNING)

#%% Imported from raw_signal_Comp2

#%%[markdown]
#
# only the 100 kHz signal is required.  
#
#%%

# I use the current working directory of the file to store the folder with the data for ease (FIR_LP_filter/).
FOLDER_FOR_DATA = Path.cwd()/'measurements_12_05_22'
if not FOLDER_FOR_DATA.exists():   
    FOLDER_FOR_DATA = Path('D:/_data/WEL/WEL20220512/')

#%%

#Constant directories and names for the .tdms file structure
tdms_f_name = 'Data.tdms'
tdms_folder_id = 'WTmeas20220512-'

#%% [markdown]
#%% CONSTANTS

GROUP_NAME = 'Wind Measurement'
CHAN_NAME = 'Torque'

#%%
# Inverter measurements 
# Dir name 
inv_meas_dir = 'Inverter'

WT_inv_1_WS_0 = '115754'
# contains the following channels
# [<TdmsChannel with path /'Wind Measurement'/'Torque'>,
#  <TdmsChannel with path /'Wind Measurement'/'Drag'>,
#  <TdmsChannel with path /'Wind Measurement'/'Wind1'>,
#  <TdmsChannel with path /'Wind Measurement'/'Wind2'>]

path_inv_meas = FOLDER_FOR_DATA / inv_meas_dir / f'{tdms_folder_id}{WT_inv_1_WS_0}' / tdms_f_name

tdms_raw_WT =TdmsFile(path_inv_meas)

df_tdms_inv_meas_1_0 = WT_NoiseChannelProc.from_tdms(tdms_raw_WT[GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter On, WS=0, 100kHz')
#%%


# Decimation folder measurments 
dec_meas_dir = 'Decimation'
dec_at_50_kHz = '121419'
dec_at_5_kHz = '121435'
path_dec_meas_50_kHz = FOLDER_FOR_DATA / dec_meas_dir / f'{tdms_folder_id}{dec_at_50_kHz}' / tdms_f_name

path_dec_meas_5_kHz = FOLDER_FOR_DATA / dec_meas_dir / f'{tdms_folder_id}{dec_at_5_kHz}' / tdms_f_name

tdms_raw_WT_50kHz =TdmsFile(path_dec_meas_50_kHz)
tdms_raw_WT_5kHz =TdmsFile(path_dec_meas_5_kHz)


df_tdms_dec_50kHz = WT_NoiseChannelProc.from_tdms(tdms_raw_WT_50kHz[GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter On, WS=0, 50kHz')
df_tdms_dec_5kHz = WT_NoiseChannelProc.from_tdms(tdms_raw_WT_5kHz[GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter On, WS=0, 5kHz')

# %%
# %matplotlib qt
# ds = df_tdms_inv_meas_1_0.raw_data()
# fs_Hz = df_tdms_inv_meas_1_0.fs_Hz
# fr_Hz = 100

# ds_100 = ds.groupby(ds.index// (fs_Hz/fr_Hz)).mean()

# plt.plot(ds.index/fs_Hz, ds, '.', alpha = 0.3)
# plt.plot(ds_100.index/fr_Hz, ds_100, '.', alpha = 1)

df_tdms_inv_meas_1_0_av100 = df_tdms_inv_meas_1_0.average(100)
print(df_tdms_inv_meas_1_0.operations)
print(df_tdms_inv_meas_1_0_av100.operations)
print(df_tdms_inv_meas_1_0.decimate(1).operations)
print(df_tdms_inv_meas_1_0.decimate(1).average(100).operations)
print(df_tdms_inv_meas_1_0.filter(fc_Hz=100).average(100).operations)
# %%
#TODO should create testing for class
# print(df_tdms_inv_meas_1_0.fs_Hz)
# print(df_tdms_inv_meas_1_0.data)
# print(df_tdms_inv_meas_1_0.data_as_Series)
# print(df_tdms_inv_meas_1_0._filter(fc_Hz=100))
# print(df_tdms_inv_meas_1_0.get_spectrum_filt(fc_Hz=100)) # graph obj
# print(df_tdms_inv_meas_1_0.get_spectrum_raw_dec(dec=1)) # graph obj

print(df_tdms_inv_meas_1_0.decimate(1).operations)
# print(df_tdms_inv_meas_1_0.get_averaged(fr_Hz=100))   #-> Obj
# %%
# %%
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Up to here 
# #%%
plot_spect_comb2([df_tdms_inv_meas_1_0.calc_spectrum_gen(dec=1, nperseg=20*1024),
                  df_tdms_inv_meas_1_0.calc_spectrum_gen(dec=2, nperseg=10*1024),
                  df_tdms_inv_meas_1_0.calc_spectrum_gen(dec=20, nperseg=1024)
                  ],
                title='Comparison of decimated signal 100kHz',
                xlim=[1e1,1e5], ylim = [1e-4,1e-0]
                )
#%% [markdown]
# ## Comparing averaging after decimation  
# comparing the signal 
# when different filters are applied and averaging occurs
#
#  this is for ws0 so we may need to look at different WS (with and without)
#%%
plot_spect_comb2([df_tdms_inv_meas_1_0.average(fr_Hz=100).calc_spectrum_gen(dec=1, nperseg=1024),
                  df_tdms_inv_meas_1_0.decimate(dec=2,offset=0).average(fr_Hz=100).calc_spectrum_gen(dec=1, nperseg=1024),
                  df_tdms_inv_meas_1_0.decimate(dec=20,offset=0).average(fr_Hz=100).calc_spectrum_gen(dec=1, nperseg=1024)
                  ],
                title='Comparison of decimated and averaged signal at WS0',
                xlim=[1e0,1e4], ylim = [1e-8,1e-2]
                )

#%% [markdown]
# ## Comparing averaging after filtering
# comparing the signal 
# when different filters are applied and averaging occurs
#%%
plot_spect_comb2([df_tdms_inv_meas_1_0.filter(fc_Hz = 100).average(fr_Hz=100).calc_spectrum_gen(dec=1, nperseg=1024),
                  df_tdms_inv_meas_1_0.filter(fc_Hz = 200).average(fr_Hz=100).calc_spectrum_gen(dec=1, nperseg=1024),
                  df_tdms_inv_meas_1_0.filter(fc_Hz = 2000).average(fr_Hz=100).calc_spectrum_gen(dec=1, nperseg=1024)
                   ],
                title='Comparison of averaging after different filters are applied ',
                xlim=[1e0,1e4], ylim = [1e-8,1e-2]
                )
#%% [markdown]
# The above procedure should be applied to files with 
# inverter on and off 
#     and 
# WS different than 0
             
#%%
# # %matplotlib inline
# %matplotlib qt



#%%
class Plotter_Class():
    #TODO Not Implemented
    """#TODOthis is a class that can take different object
    and takes their raw data and plot:
    - Time histories
    - spectrums 
    """    
    pass



#%% [markdown]
#------------------------------------------------------------------
# # Averaging comparison for Compressed air dataset.
# The above procedure should be applied to files with 
# inverter on and off 
#     and 
# WS different than 0


# %%
#CONSTANTS

 #  I use the current working directory of the file to store the folder with the data for ease (FIR_LP_filter/).
 # FOLDER_FOR_DATA = Path.cwd()/'measurements_12_05_22'
 # FOLDER_FOR_DATA = Path('D:/_data/WEL/WEL20220512/')

# Update for automated path detection


# If you prefear another folder for storing the data use this
# the last line will join the names like a path from the system
#  
# home_folder = Path.home()
# dir_no_1 = 'folder name as a string'
# dir_no_2 = '.....'
# dir_no_3 = '.....' 
# dir_no_4 = '.....'
#
#FOLDER_FOR_DATA = home_folder / dir_no_1 / dir_no_2 / dir_no_3 / dir_no_4 / ..... / .....


#Constant directories and names for the .tdms file structure
tdms_folder_id = 'WTmeas20220512-'
tdms_f_name = 'Data.tdms'

# Dir names for the Compressed air measurment
comp_air_dir = 'compressed air'

data_CA_inv_0_WS_0 = '112318'
data_CA_inv_0_WS_5 = '112629'
data_CA_inv_0_WS_11= '112709'
data_CA_inv_1_WS_0 = '113005' 
data_CA_inv_1_WS_5 = '113534'
data_CA_inv_1_WS_10= '113614'

path_comp = FOLDER_FOR_DATA / comp_air_dir / tdms_folder_id

# CA stands for compressed air

raw_signal_CA = [data_CA_inv_0_WS_0, data_CA_inv_0_WS_5, 
                data_CA_inv_0_WS_11, data_CA_inv_1_WS_0,
                data_CA_inv_1_WS_5, data_CA_inv_1_WS_10 ]

tdms_raw_CA = []

for item in raw_signal_CA:
    y = f'{path_comp}{item}'
    x=TdmsFile( Path( y , tdms_f_name))
    tdms_raw_CA.append(x)


GROUP_NAME = 'Wind Measurement'
CHAN_NAME = 'Torque'

# df_tdms_0_0 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[0][GROUP_NAME][CHAN_NAME]
#                 , desc= 'Inverter off, WS=0')
df_tdms_0_5 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[1][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter off, WS=5')
# df_tdms_0_11 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[2][GROUP_NAME][CHAN_NAME]
#                 , desc= 'Inverter off, WS=11')
# df_tdms_1_0 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[3][GROUP_NAME][CHAN_NAME]
#                 , desc= 'Inverter on, WS=0')
df_tdms_1_5 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[4][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter on, WS=5')
# df_tdms_1_10 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[5][GROUP_NAME][CHAN_NAME]
                # , desc= 'Inverter on, WS=10')

#%%
#TODO consider renaming df_tdms_0_0 to df_tdms_i0_w0
# where i: inverter state
# where w: wind speed

#%%
# Estimate the power spectral density of the raw signal
# Hotwire speed 0 m/s
NPERSEG=1024
fc_Hz=200
fr_HZ = 100
#%%
plot_spect_comb2([df_tdms_0_5.calc_spectrum(nperseg=NPERSEG*20),
                df_tdms_0_5.decimate(2).calc_spectrum(nperseg=NPERSEG*10),
                df_tdms_0_5.decimate(20).calc_spectrum(nperseg=NPERSEG)], 
                 title='Comparison of spectra for signals at WS=5 for inverter Off \n decimated ',
                     xlim =[1e2,3e5], ylim= [1e-7,1e-2],
                Kolmogorov_offset=1e3, to_disk=True)

#%%
plot_spect_comb2([df_tdms_0_5.average(fr_Hz=fr_HZ).calc_spectrum(nperseg=NPERSEG/4),
                df_tdms_0_5.decimate(2).average(fr_Hz=fr_HZ).calc_spectrum(nperseg=NPERSEG/4),
                df_tdms_0_5.decimate(20).average(fr_Hz=fr_HZ).calc_spectrum(nperseg=NPERSEG/4)], 
                title='Comparison of spectra for signals at WS=5 for inverter Off \n decimated  and averaged',
                xlim =[1e0,3e2], ylim= [1e-7,1e-2],
                Kolmogorov_offset=2e-2, to_disk=True)
#%%
plot_spect_comb2([df_tdms_0_5.filter(fc_Hz=fc_Hz).average(fr_Hz=fr_HZ).calc_spectrum(nperseg=NPERSEG/4),
                df_tdms_0_5.decimate(2).filter(fc_Hz=fc_Hz, desc = 'dec.f:2, fc:100').average(fr_Hz=fr_HZ).calc_spectrum(nperseg=NPERSEG/4),
                df_tdms_0_5.decimate(20).filter(fc_Hz=fc_Hz,desc = 'dec.f:20, fc:100').average(fr_Hz=fr_HZ).calc_spectrum(nperseg=NPERSEG/4)], 
                 title='Comparison of spectra for signals at WS=5 for inverter Off \n decimated, filtered and finally averaged ',
                     xlim =[1e0,3e2], ylim= [1e-7,1e-2],
                Kolmogorov_offset=2e-2, to_disk=True)


# %% [markdown]
# plotting Inverter on measurements at WS 5 m/s
# 
# %%  ===========================================================

plot_spect_comb2([df_tdms_1_5.calc_spectrum(nperseg=NPERSEG*20),
                df_tdms_1_5.decimate(2).calc_spectrum(nperseg=NPERSEG*10),
                df_tdms_1_5.decimate(20).calc_spectrum(nperseg=NPERSEG)], 
                 title='Comparison of spectra for signals at WS=5 for inverter On \n decimated ',
                     xlim =[1e2,3e5], ylim= [1e-5,1e-1],
                Kolmogorov_offset=1e3, to_disk=True)
# %%

plot_spect_comb2([df_tdms_1_5.average(fr_Hz=fr_HZ).calc_spectrum(nperseg=NPERSEG/4),
                df_tdms_1_5.decimate(2).average(fr_Hz=fr_HZ).calc_spectrum(nperseg=NPERSEG/4),
                df_tdms_1_5.decimate(20).average(fr_Hz=fr_HZ).calc_spectrum(nperseg=NPERSEG/4)], 
                title='Comparison of spectra for signals at WS=5 for inverter On \n decimated  and averaged',
                xlim =[1e0,3e2], ylim= [1e-7,1e-2],
                Kolmogorov_offset=2e-2, to_disk=True)
#%%
fc_Hz = 10
plot_spect_comb2([df_tdms_1_5.filter(fc_Hz=fc_Hz).average(fr_Hz=fr_HZ).calc_spectrum(nperseg=NPERSEG/4),
                df_tdms_1_5.decimate(2).filter(fc_Hz=fc_Hz, desc = 'dec.f:2, fc:100').average(fr_Hz=fr_HZ).calc_spectrum(nperseg=NPERSEG/4),
                df_tdms_1_5.decimate(20).filter(fc_Hz=fc_Hz,desc = 'dec.f:20, fc:100').average(fr_Hz=fr_HZ).calc_spectrum(nperseg=NPERSEG/4)], 
                title='Comparison of spectra for signals at WS=5 for inverter On \n decimated, filtered and finally averaged ',
                xlim =[1e0,3e2], ylim= [1e-7,1e-2],
                Kolmogorov_offset=2e-2, to_disk=True)
# %%
