#%% [markdown]
# the aim of this file is to investigate the effect of sampling frequency
# more specifically if the usb card when lowering the frequency behaves in a different  manner observable in the PS
#
# The comparison will revolve aroudn wind speed 0 measurements and more spe:
# - ca_1_0 
# - de50.1
# - de5.1
#%%
from pathlib import Path
from matplotlib import pyplot as plt
import scipy.signal as signal
import numpy as np
import pandas as pd

from nptdms import TdmsFile

from pros_noisefiltering.gen_functions import spect,  plot_spect_comb2
from pros_noisefiltering.Graph_data_container import  Graph_data_container
from pros_noisefiltering.WT_NoiProc import WT_NoiseChannelProc, filt_butter_factory, plot_comparative_response

filter_Butter_default=filt_butter_factory(filt_order = 2, fc_hz = 100)


import logging
logging.basicConfig( level=logging.WARNING)

#%%[markdown]
#
# only the 100 kHz signal is required.  
#
#%%

# I use the current working directory of the file to store the folder with the data for ease (FIR_LP_filter/).
FOLDER_FOR_DATA = Path.cwd()/'measurements_12_05_22'
if not FOLDER_FOR_DATA.exists():   
    FOLDER_FOR_DATA = Path('D:/_data/WEL/WEL20220512/')

#%% CONSTANTS
TDMS_FNAME = 'Data.tdms'
GROUP_NAME = 'Wind Measurement'
CHAN_NAME = 'Wind2'


#%% [markdown]
# Inverter measurements 

# Dir name 
#Constant directories and names for the .tdms file structure
ca_meas_dir = FOLDER_FOR_DATA / 'compressed air'

data_CA_inv_1_WS_0 = 'ca1_0.1'
# contains the following channels
# [<TdmsChannel with path /'Wind Measurement'/'Torque'>,
#  <TdmsChannel with path /'Wind Measurement'/'Drag'>,
#  <TdmsChannel with path /'Wind Measurement'/'Wind1'>,
#  <TdmsChannel with path /'Wind Measurement'/'Wind2'>]

path_ca_meas = ca_meas_dir / f'{data_CA_inv_1_WS_0}' / TDMS_FNAME

tdms_raw_WT =TdmsFile(path_ca_meas)

ca1_0 = WT_NoiseChannelProc.from_tdms(tdms_raw_WT[GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter On, WS=0, 500kHz')
#%%


# Decimation folder measurments 
dec_meas_dir = FOLDER_FOR_DATA / 'Decimation'
dec_at_50_kHz = 'de50.1'
dec_at_5_kHz = 'de5.1'
path_dec_meas_50_kHz = dec_meas_dir / f'{dec_at_50_kHz}' / TDMS_FNAME

path_dec_meas_5_kHz = FOLDER_FOR_DATA / dec_meas_dir / f'{dec_at_5_kHz}' / TDMS_FNAME

tdms_raw_WT_50kHz =TdmsFile(path_dec_meas_50_kHz)
tdms_raw_WT_5kHz =TdmsFile(path_dec_meas_5_kHz)


dec_50kHz = WT_NoiseChannelProc.from_tdms(tdms_raw_WT_50kHz[GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter On, WS=0, 50kHz')
dec_5kHz = WT_NoiseChannelProc.from_tdms(tdms_raw_WT_5kHz[GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter On, WS=0, 5kHz')

# %%
# %matplotlib qt

in1_0_av100 = ca1_0.average(100)
print(ca1_0.operations)
print(in1_0_av100.operations)
print(ca1_0.decimate(1).operations)
print(ca1_0.decimate(1).average(100).operations)
print(ca1_0.filter(fc_hz=100).average(100).operations)
# %%
#TODO should create testing for class
# print(in1_0.fs_hz)
# print(in1_0.data)
# print(in1_0.data_as_Series)
# print(in1_0._filter(fc_hz=100))
# print(in1_0.get_spectrum_filt(fc_hz=100)) # graph obj
# print(in1_0.get_spectrum_raw_dec(dec=1)) # graph obj

print(ca1_0.decimate(1).operations)
# print(in1_0.get_averaged(fr_Hz=100))   #-> Obj
# %% [markdown]
# This takes 
#%%
NPERSEG=1024<<6
FIGSIZE = (15,10)
plot_spect_comb2([ca1_0.decimate(dec=1,offset=0).set_desc('500 kHz').calc_spectrum( nperseg=NPERSEG),
                  ca1_0.decimate(dec=10,offset=0).set_desc('50 kHz (dec=10)').calc_spectrum( nperseg=NPERSEG/10),
                  ca1_0.decimate(dec=100,offset=0).set_desc('5 kHz (dec=100)').calc_spectrum( nperseg=NPERSEG/100)
                  ],
                title='Comparison of decimated signal 500kHz by two orders of magnitude',
                xlim=[1e1,2.5e5], ylim = [1e-5,0.5e-2],
                figsize = FIGSIZE,
                draw_lines=True
                )

#%% [markdown]
# ## Comparing compressed air with other measurements with less sampling frequency
# comparing the signal 
# when different filters are applied and averaging occurs
#

plot_spect_comb2([ca1_0.set_desc('500 kHz').calc_spectrum( nperseg=NPERSEG),
                  dec_50kHz.set_desc('50 kHz').calc_spectrum( nperseg=NPERSEG/10),
                  dec_5kHz.set_desc('5 kHz').calc_spectrum( nperseg=NPERSEG/100)
                  ],
                title='Comparison of signals with different sampling rates',
                xlim=[1e1,2.5e5], ylim = [1e-5,0.5e-2],
                figsize = FIGSIZE
                , draw_lines=True
                )
             
#%%[markdown ]
# Compare time histories for dec5kHz with 500kHz
#%%
# # %matplotlib inline
# %matplotlib qt

def compare_timehistories(df_ni,df_wi, final_point = 100000,
    stitle='', fname:str =None, figsize=(15,10)):
    """plots a comparison of time histories to observe the effect of the inverter. 
    

    Args:
        df_ni (_type_): data set  without inverter
        df_wi (_type_): data set  with inverter
        final_point (_type_, optional): _description_. Defaults to 100000stitle=''.
    """    
    final_point2 = int(df_wi.fs_hz/df_ni.fs_Hz*final_point)
    fig, axs = plt.subplots(1,2, sharey=True, figsize= figsize)
     # -1 for 
    axs[0].plot(df_ni.data_as_Series[:final_point].index/df_ni.fs_hz, df_ni.data_as_Series[:final_point], '.', alpha=0.3)
    axs[0].set_ylabel('Transducer Voltage')
    axs[0].set_xlabel('Measurement No')
    axs[0].grid('both')
    axs[0].set_title(df_ni.description)

    axs[1].plot(df_wi.data_as_Series[:final_point2].index/df_wi.fs_hz, df_wi.data_as_Series[:final_point2], '.', alpha=0.3)
    axs[1].set_xlabel('Measurement No')
    axs[1].set_ylabel('Transducer Voltage')
    axs[1].grid('both')
    axs[1].set_title(df_wi.description)
    plt.suptitle(stitle)
    if fname is not None:
        fullfname = f'_temp_fig/{fname}.png'
        plt.savefig(fullfname)
#%%
compare_timehistories(ca1_0,dec_5kHz, stitle='Time history comparison:  WS=0 m/s',fname='s1_Comp_th-ws0.png')

#%%