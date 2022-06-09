#%% [markdown]
# show a comparison of the signal with and without the inverter on.
# 
# this uses inverter measurements 1 and 2
# 
#%%
from pathlib import Path
from matplotlib import pyplot as plt
import scipy.signal as signal
import numpy as np
import pandas as pd

import nptdms
from nptdms import TdmsFile

from functions import spect,  plot_spect_comb2, Graph_data_container
from WT_NoiProc import WT_NoiseChannelProc, filt_butter_factory
filter_Butter_default=filt_butter_factory(filt_order = 2, fc_Hz = 100)


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

#%% CONSTANTS
FIGSIZE_STD = (12,6)
#Constant directories and names for the .tdms file structure
# Dir name 
GRP_MEAS_DIR = 'Inverter'
TMDS_FOLDER_PREFIX = 'WTmeas20220512-'
TDMS_FNAME = 'Data.tdms'
GROUP_NAME = 'Wind Measurement'
CHAN_NAME = 'Wind1'

#%%
# Inverter measurements of interest
WT_inv_0_WS_0 = '115657'
WT_inv_1_WS_0 = '115754'

path_comp = FOLDER_FOR_DATA / GRP_MEAS_DIR / TMDS_FOLDER_PREFIX

# suffixes:
# - CA : compressed air
# - Inv : Inverter
# - DEC : decimation

raw_signal_Inv = [WT_inv_0_WS_0, WT_inv_1_WS_0]

l_tdms_Inv = []

for item in raw_signal_Inv:
    x=TdmsFile( Path( f'{path_comp}{item}' , TDMS_FNAME))
    l_tdms_Inv.append(x)
    
#%%    
[print(x) for x in l_tdms_Inv[0][GROUP_NAME].channels()]
# %%
df_inv_i0_w0 = WT_NoiseChannelProc.from_tdms(l_tdms_Inv[0][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter Off, WS=0, 100kHz')
df_inv_i1_w0 = WT_NoiseChannelProc.from_tdms(l_tdms_Inv[1][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter On, WS=0, 100kHz')
# %%

fig, axs = plt.subplots(1,2, sharey=True, figsize= FIGSIZE_STD)
final_point = 10000 # -1 for 
axs[0].plot(df_inv_i0_w0.data_as_Series[:final_point], '.', alpha=0.3)
axs[0].set_ylabel('Transducer Voltage')
axs[0].set_xlabel('Measurement No')
axs[0].grid('both')
axs[0].set_title('Inverter Off - WS=0')

axs[1].plot(df_inv_i1_w0.data_as_Series[:final_point], '.', alpha=0.3)
axs[1].set_xlabel('Measurement No')
axs[1].set_ylabel('Transducer Voltage')
axs[1].grid('both')
axs[1].set_title('Inverter On - WS=0')
plt.savefig(f'_temp_fig/_Step_1-Comparison-{final_point}pts.png')
# %% [markdown ]
# Power spectrums

# %%
fig, axs = plt.subplots(1,1, sharey=True, figsize= FIGSIZE_STD)
final_point = -1  # -1 for 
axs.plot(df_inv_i0_w0.calc_spectrum(), '.', alpha=0.3)
axs.plot(df_inv_i0_w0.calc_spectrum(), '.', alpha=0.3)
axs.set_ylabel('Transducer Voltage')
axs.set_xlabel('Measurement No')
axs.grid('both')
axs.set_title('Inverter Off - WS=0')
plt.savefig(f'_temp_fig/_Step_2-Comparison-SPec {final_point}pts.png')