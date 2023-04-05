#%% [markdown]
# shows the effect on the inverter filtered data
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
from pros_noisefiltering.WT_NoiProc import {WT_NoiseChannelProc,
                                            filt_butter_factory,
                                            plot_comparative_response}
# filter_Butter_default=filt_butter_factory(filt_order = 2, fc_hz = 100)

import logging
logging.basicConfig( level=logging.WARNING)

#%%[markdown]
#
# only the 100 kHz signal is required.  
#
#%%

# I use the current working directory of the file to store the folder with the data for ease (FIR_LP_filter/).
FOLDER_FOR_DATA = Path('/mnt/data_folder')/'measurements_12_05_22/new_record_prop_channel/'
if not FOLDER_FOR_DATA.exists():   
    FOLDER_FOR_DATA = Path('D:/_data/WEL/WEL20220512/')

#%% CONSTANTS
FIGSIZE_STD = (6,6)
#Constant directories and names for the .tdms file structure
# Dir name 
TDMS_FNAME = 'Data.tdms'
GROUP_NAME = 'Wind Measurement'
CHAN_NAME = 'Wind2'

#%%
inv_meas_dir = 'inverter'
# Inverter measurements of interest
data_inv_inv_0_WS_0= 'in0_0.1'
data_inv_inv_1_WS_0 = 'in1_0.1'
data_inv_inv_1_WS_5 = 'in1_5.1'
data_inv_inv_1_WS10= 'in1_10.1'
data_inv_inv_1_WS15 = 'in1_15.1' 
data_inv_inv_1_WS_20 = 'in1_20.1'


path_comp = FOLDER_FOR_DATA / inv_meas_dir 

# suffixes:
# - CA : compressed air
# - Inv : Inverter
# - DEC : decimation

raw_signal_CA = [data_inv_inv_0_WS_0, data_inv_inv_1_WS_0,
                 data_inv_inv_1_WS_5, 
                data_inv_inv_1_WS10, data_inv_inv_1_WS15,
                data_inv_inv_1_WS_20 ]

l_tdms_Inv = []

for item in raw_signal_CA:
    x=TdmsFile( Path( f'{path_comp}/{item}' , TDMS_FNAME))
    l_tdms_Inv.append(x)
    
#%%    
[print(x) for x in l_tdms_Inv[0][GROUP_NAME].channels()]
# %%
dfi_i0_w0 = WT_NoiseChannelProc.from_tdms(l_tdms_Inv[0][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter Off, WS=0, 100kHz')
dfi_i1_w0 = WT_NoiseChannelProc.from_tdms(l_tdms_Inv[1][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter On, WS=0, 100kHz')
dfi_i1_w5 = WT_NoiseChannelProc.from_tdms(l_tdms_Inv[2][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter On, WS=5, 100kHz')
dfi_i1_w10 = WT_NoiseChannelProc.from_tdms(l_tdms_Inv[3][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter On, WS=10, 100kHz')
dfi_i1_w15 = WT_NoiseChannelProc.from_tdms(l_tdms_Inv[4][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter On, WS=15, 100kHz')
dfi_i1_w20 = WT_NoiseChannelProc.from_tdms(l_tdms_Inv[5][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter On, WS=20, 100kHz')
# %%

# %% [markdown ]
# Power spectrums


# %%
NPERSEG = 1024
filter_Butter_200=filt_butter_factory(filt_order = 2, fc_hz = 200)
xlims=  [1e0,1e5]


# %%
plot_comparative_response(dfi_i0_w0, # cutoff frequency
        filter_func=filter_Butter_200, 
        response_offset=2e-4,            
        Kolmogorov_offset = 4e-2,
        nperseg=NPERSEG*100
        , xlim=xlims
        ,figsize =(12,8))
# plt.savefig(f'_temp_fig/s6-PS-WS00-filt{filter_Butter_200.params.get("fc_hz")}',facecolor='white', transparent=False)

#%%
plot_comparative_response(dfi_i1_w0, # cutoff frequency
        filter_func=filter_Butter_200, 
        response_offset=2e-4,            
        Kolmogorov_offset = 4e-2,
        nperseg=NPERSEG*100
        , xlim=xlims
        ,figsize =(12,8))
# plt.savefig(f'_temp_fig/s6-PS-WS05-filt{filter_Butter_200.params.get("fc_hz")}',facecolor='white', transparent=False)

#%%
plot_comparative_response(dfi_i1_w5, # cutoff frequency
        filter_func=filter_Butter_200, 
        response_offset=2e-4,            
        Kolmogorov_offset = 4e-2,
        nperseg=NPERSEG*100
        , xlim=xlims
        ,figsize =(12,8))

# %%
plot_comparative_response(dfi_i1_w10, # cutoff frequency
        filter_func=filter_Butter_200, 
        response_offset=2e-4,            
        Kolmogorov_offset = 4e-2,
        nperseg=NPERSEG*100
        , xlim=xlims
        ,figsize =(12,8))

# %%
plot_comparative_response(dfi_i1_w15, # cutoff frequency
        filter_func=filter_Butter_200, 
        response_offset=2e-4,            
        Kolmogorov_offset = 4e-2,
        nperseg=NPERSEG*100
        , xlim=xlims
        ,figsize =(12,8))


# %%
plot_comparative_response(dfi_i1_w20, # cutoff frequency
        filter_func=filter_Butter_200, 
        response_offset=2e-3,            
        Kolmogorov_offset = 4e-0,
        nperseg=NPERSEG*100,
        xlim=xlims
        ,figsize =(12,8))


# %%
plt.show()
