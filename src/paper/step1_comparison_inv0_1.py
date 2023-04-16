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
FOLDER_FOR_DATA = Path(
    '/mnt/data_folder/measurements_12_05_22/new_record_prop_channel/')
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
def compare_timehistories(df_ni,df_wi, final_point = 100000,
    stitle='', fname:str =None):
    """_summary_

    Args:
        df_ni (_type_): data set  without inverter
        df_wi (_type_): data set  with inverter
        final_point (_type_, optional): _description_. Defaults to 100000stitle=''.
    """    
    """plots a comparison of time histories to observe the effect of the inverter. 
    
    """    
    fig, axs = plt.subplots(1,2, sharey=True, figsize= FIGSIZE_STD)
     # -1 for 
    axs[0].plot(df_ni.data_as_Series[:final_point], '.', alpha=0.3)
    axs[0].set_ylabel('Transducer Voltage')
    axs[0].set_xlabel('Measurement No')
    axs[0].grid('both')
    axs[0].set_title(df_ni.description)

    axs[1].plot(df_wi.data_as_Series[:final_point], '.', alpha=0.3)
    axs[1].set_xlabel('Measurement No')
    axs[1].set_ylabel('Transducer Voltage')
    axs[1].grid('both')
    axs[1].set_title(df_wi.description)
    plt.suptitle(stitle)
    if fname is not None:
        fullfname = f'_temp_fig/{fname}.png'
        plt.savefig(fullfname)
#%%
compare_timehistories(df_ca_i0_w0,df_ca_i1_w0, stitle='Time history comparison:  WS=0 m/s',fname='s1_Comp_th-ws0.png')
compare_timehistories(df_ca_i0_w10,df_ca_i1_w10, stitle='Time history comparison:  WS=10 m/s',fname='s1_Comp_th-ws10.png')
#%%





# %% [markdown ]
# Power spectrums


# %%
NPERSEG_DEF = 1024<<8

plot_spect_comb2([df_ca_i0_w0.set_desc('Inverter Off').calc_spectrum(nperseg=NPERSEG_DEF)],
                title = 'Power Spectrum  for Inverter Off at WS=0, fs=500kHz',
                xlim =[1e0,3e5], ylim= [1e-7,1e-1],
                Kolmogorov_offset=1e-2, 
                figsize = FIGSIZE_STD,
                markersize=5,
                alpha =1,
                markers = ['.','.','_']
                , draw_lines=True
                , fname = 'S2_Comp_PS_WS0_i0'
                )

plot_spect_comb2([            df_ca_i1_w0.set_desc('Inverter On').calc_spectrum(nperseg=NPERSEG_DEF)],
                title = 'Power Spectrum  for Inverter On at WS=0, fs=500kHz',
                xlim =[1e0,3e5], ylim= [1e-7,1e-1],
                Kolmogorov_offset=1e-2, 
                figsize = FIGSIZE_STD,
                markersize=5,
                alpha =1,
                markers = ['.','.','_']
                , draw_lines=True
                ,fname = 'S2_Comp_PS_WS0_i1')
#%%
plot_spect_comb2([df_ca_i0_w0.set_desc('Inverter Off').calc_spectrum(nperseg=NPERSEG_DEF),
            df_ca_i1_w0.set_desc('Inverter On').calc_spectrum(nperseg=NPERSEG_DEF)],
                title = 'Power Spectrum comparison for Inverter On/Off at WS=0, fs=500kHz',
                xlim =[1e0,3e5], ylim= [1e-7,1e-1],
                Kolmogorov_offset=1e-2, 
                figsize = FIGSIZE_STD,
                markersize=15,
                alpha =1,
                markers = ['o','.','_'],
                fname = 'S2_Comp_PS_WS0')
# %%
plot_spect_comb2([df_ca_i0_w5.set_desc('Inverter Off').calc_spectrum(nperseg=NPERSEG_DEF),
                  df_ca_i1_w5.set_desc('Inverter On').calc_spectrum(nperseg=NPERSEG_DEF)],
                title = 'Power Spectrum comparison for Inverter On/Off at WS=5, fs=500kHz',
                xlim =[1e0,3e5], ylim= [1e-7,1e-1],
                Kolmogorov_offset=1e-0, 
                figsize = FIGSIZE_STD,
                markersize=15,
                alpha=0.3,
                markers = ['o','.','_'],
                fname = 'S2_Comp_PS_WS5')

# %%

plot_spect_comb2([df_ca_i0_w10.set_desc('Inverter Off').calc_spectrum(nperseg=NPERSEG_DEF),
                  df_ca_i1_w10.set_desc('Inverter On').calc_spectrum(nperseg=NPERSEG_DEF)],
                title = 'Power Spectrum comparison for Inverter On/Off at WS=10, fs=500kHz',
                xlim =[1e0,3e5], ylim= [1e-7,1e-1],
                Kolmogorov_offset=2e0,
                figsize = FIGSIZE_STD,
                markersize=15,
                markers = ['o','.','_'],
                fname = 'S2_Comp_PS_WS10')
# %%



plot_spect_comb2([df_ca_i0_w10.set_desc('Inverter Off').calc_spectrum(nperseg=NPERSEG_DEF),
                  df_ca_i1_w10.set_desc('Inverter On').calc_spectrum(nperseg=NPERSEG_DEF)],
                title = 'Power Spectrum comparison for Inverter On/Off at WS=10, fs=500kHz',
                xlim =[1e0,3e5], ylim= [1e-7,1e-1],
                Kolmogorov_offset=2e0,
                figsize = (12,5),
                markersize=15,
                markers = ['o','.','_'],
                fname = 'S2_Comp_PS_WS10-wide')
# %%

plt.show()
