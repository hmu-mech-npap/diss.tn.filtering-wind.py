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

from nptdms import TdmsFile


from pros_noisefiltering.gen_functions import spect, plot_spect_comb2
from pros_noisefiltering.Graph_data_container import Graph_data_container
from pros_noisefiltering.WT_NoiProc import WT_NoiseChannelProc, filt_butter_factory, plot_comparative_response
filter_Butter_default=filt_butter_factory(filt_order = 2, fc_Hz = 100)

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
FIGSIZE_STD = (12,6)
#Constant directories and names for the .tdms file structure
# Dir name 
TDMS_FNAME = 'Data.tdms'
GROUP_NAME = 'Wind Measurement'
CHAN_NAME = 'Wind2'

#%%
ca_meas_dir = 'compressed air'
# Inverter measurements of interest
data_CA_inv_0_WS_0 = 'ca0_0.1'
data_CA_inv_0_WS_5 = 'ca0_5.1'
data_CA_inv_0_WS_11= 'ca0_10.1'
data_CA_inv_1_WS_0 = 'ca1_0.1' 
data_CA_inv_1_WS_5 = 'ca1_5.1'
data_CA_inv_1_WS_10= 'ca1_10.1'


path_comp = FOLDER_FOR_DATA / ca_meas_dir 

# suffixes:
# - CA : compressed air
# - Inv : Inverter
# - DEC : decimation

raw_signal_CA = [data_CA_inv_0_WS_0, data_CA_inv_0_WS_5, 
                data_CA_inv_0_WS_11, data_CA_inv_1_WS_0,
                data_CA_inv_1_WS_5, data_CA_inv_1_WS_10 ]

l_tdms_Inv = []

for item in raw_signal_CA:
    x=TdmsFile( Path( f'{path_comp}/{item}' , TDMS_FNAME))
    l_tdms_Inv.append(x)
    
#%%    
[print(x) for x in l_tdms_Inv[0][GROUP_NAME].channels()]
# %%
df_ca_i0_w0 = WT_NoiseChannelProc.from_tdms(l_tdms_Inv[0][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter Off, WS=0, 500kHz')
df_ca_i0_w5 = WT_NoiseChannelProc.from_tdms(l_tdms_Inv[1][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter Off, WS=5, 500kHz')
df_ca_i0_w10 = WT_NoiseChannelProc.from_tdms(l_tdms_Inv[2][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter Off, WS=10, 500kHz')
df_ca_i1_w0 = WT_NoiseChannelProc.from_tdms(l_tdms_Inv[3][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter On, WS=0, 500kHz')
df_ca_i1_w5 = WT_NoiseChannelProc.from_tdms(l_tdms_Inv[4][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter On, WS=5, 500kHz')
df_ca_i1_w10 = WT_NoiseChannelProc.from_tdms(l_tdms_Inv[5][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter On, WS=10, 500kHz')
# %%

fig, axs = plt.subplots(1,2, sharey=True, figsize= FIGSIZE_STD)
final_point = 100000 # -1 for 
axs[0].plot(df_ca_i0_w0.data_as_Series[:final_point], '.', alpha=0.3)
axs[0].set_ylabel('Transducer Voltage')
axs[0].set_xlabel('Measurement No')
axs[0].grid('both')
axs[0].set_title('Inverter Off - WS=0')

axs[1].plot(df_ca_i1_w0.data_as_Series[:final_point], '.', alpha=0.3)
axs[1].set_xlabel('Measurement No')
axs[1].set_ylabel('Transducer Voltage')
axs[1].grid('both')
axs[1].set_title('Inverter On - WS=0')
plt.savefig(f'_temp_fig/_Step_1-Comparison-{final_point}pts.png')
# %% [markdown ]
# Power spectrums


# %%
plot_spect_comb2([df_ca_i0_w0.calc_spectrum(),df_ca_i1_w0.calc_spectrum()],
                title = 'Power Spectrum comparison for Inverter On/Off at WS=0',
                xlim =[1e2,3e5], ylim= [1e-4,1e-2],
                Kolmogorov_offset=1e3, to_disk=True,figsize = FIGSIZE_STD,
                markersize=15,
                markers = ['.','x','_'])
# %%
plot_spect_comb2([df_ca_i0_w5.calc_spectrum(),df_ca_i1_w5.calc_spectrum()],
                title = 'Power Spectrum comparison for Inverter On/Off at WS=5',
                xlim =[1e2,3e5], ylim= [1e-4,1e-2],
                Kolmogorov_offset=1e3, to_disk=True,figsize = FIGSIZE_STD,
                markersize=15,
                markers = ['.','x','_'])

# %%
NPERSEG_DEF = 1024<<8
plot_spect_comb2([df_ca_i0_w10.calc_spectrum(nperseg=NPERSEG_DEF),
                  df_ca_i1_w10.calc_spectrum(nperseg=NPERSEG_DEF)],
                title = 'Power Spectrum comparison for Inverter On/Off at WS=10',
                xlim =[1e1,3e5], ylim= [1e-6,1e-1],
                Kolmogorov_offset=2e0, to_disk=True,figsize = FIGSIZE_STD,
                markersize=15,
                markers = ['.','x','_'])
# %%
