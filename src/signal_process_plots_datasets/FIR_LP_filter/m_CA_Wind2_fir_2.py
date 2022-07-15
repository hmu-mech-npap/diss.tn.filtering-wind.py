#%%
# File for looking at FIR filtering options
#  
#
# %%
# Functions and variables to be imported
import numpy as np
import pandas as pd
from pathlib import Path
from nptdms import TdmsFile
from scipy import signal
# from func_fir import lp_firwin
# from scipy import signal
# This is bad practice... import the classes and do the stuff properly
# from raw_signal_comp import df_tdms_0_0, df_tdms_1_0, df_tdms_0_5, df_tdms_1_5, df_tdms_0_11, df_tdms_1_10, f_spect_tdms_CA, Px_x_tdms_CA

# Old import from functions.py
# from functions import (WT_NoiseChannelProc.from_tdms, Graph_data_container,
#                         plot_signals, spect, plot_spect_comb2)

from pros_noisefiltering.WT_NoiProc import WT_NoiseChannelProc
from pros_noisefiltering.Graph_data_container import Graph_data_container
from pros_noisefiltering.gen_functions import plot_spect_comb2, spect
from pros_noisefiltering.filters import fir

#%%
# I use the current working directory of the file to store the folder with the data for ease (FIR_LP_filter/).
FOLDER_FOR_DATA = Path('/mnt/data_folder')/'measurements_12_05_22/new_record_prop_channel/'
if not FOLDER_FOR_DATA.exists():   
    FOLDER_FOR_DATA = Path('D:/_data/WEL/WEL20220512/')

#Constant directories and names for the .tdms file structure
tdms_folder_id = 'WTmeas20220512-'
tdms_f_name = 'Data.tdms'

# Dir names for the Compressed air measurment
comp_air_dir = 'compressed air'


# New measurements with renamed folders for future rec version information
data_CA_inv_0_WS_0 = 'ca0_0.1'
data_CA_inv_0_WS_5 = 'ca0_5.1'
data_CA_inv_0_WS_11= 'ca0_10.1'
data_CA_inv_1_WS_0 = 'ca1_0.1' 
data_CA_inv_1_WS_5 = 'ca1_5.1'
data_CA_inv_1_WS_10= 'ca1_10.1'

path_comp = FOLDER_FOR_DATA / comp_air_dir

# CA stands for compressed air

raw_signal_CA = [data_CA_inv_0_WS_0, data_CA_inv_0_WS_5, 
                data_CA_inv_0_WS_11, data_CA_inv_1_WS_0,
                data_CA_inv_1_WS_5, data_CA_inv_1_WS_10 ]

tdms_raw_CA = []

for item in raw_signal_CA:
    y = f'{path_comp}/{item}'
    x=TdmsFile( Path( y , tdms_f_name))
    tdms_raw_CA.append(x)


GROUP_NAME = 'Wind Measurement'
CHAN_NAME = 'Wind2'

# rename the variables to add index of number in the name as you proposed

df_tdms_i0_w0 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[0][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter off, WS=0')
df_tdms_i0_w5 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[1][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter off, WS=5')
df_tdms_i0_w11 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[2][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter off, WS=11')
df_tdms_i1_w0 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[3][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter on, WS=0')
df_tdms_i1_w5 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[4][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter on, WS=5')
df_tdms_i1_w10 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[5][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter on, WS=10')


# Define a class for FIR operations like 
def fir_filter(ds:np.ndarray,time:np.ndarray, fs_hz:float,
                fc_hz = 0.0002, filt_order = 20):
    filt_coeff, w, h = fir.lp_firwin(filt_order,fs_hz,fc_hz)
    filt_data = signal.lfilter(filt_coeff, 1.0, ds)
    warmup = filt_order-1
    uncorrupted_output = filt_data[warmup:]
    filt_sig_time_int = time[warmup:]-((warmup/2)/fs_hz)
    
    return uncorrupted_output, filt_sig_time_int

class Fir_filter:
    def __init__(self,signals) -> None:
    
        self.raw = signals.data
        #self.time_int = np.linspace(0, 7, len(self.raw))
        self.description = signals.description
        self._channel_data= signals._channel_data
        self.fs_Hz = int (1/signals._channel_data.properties['wf_increment'])
        self.channel_name = signals._channel_data.name
        self.time_int = np.linspace(0, len (self.raw) / int(self.fs_Hz), len(self.raw))
    
    def apply_fir(self, fc_hz):
        filtered, filt_time_int = fir_filter(self.raw,time=self.time_int, fs_hz=self.fs_Hz, fc_hz=fc_hz)
        return pd.Series(filtered, name=f'{self.channel_name}:filt_fc_{fc_hz}')
    
    def output_time_dur(self, fc_hz):
        filtered, filt_time_int = fir_filter(self.raw,time=self.time_int, fs_hz=self.fs_Hz, fc_hz=fc_hz)
        return filt_time_int
    
    def get_spect_fir_output(self, fc_hz):
        x_filt, y_filt = spect(self.apply_fir(fc_hz=fc_hz), FS= self.fs_Hz)
        filt_type = 'FIR'
        return Graph_data_container(x=x_filt,y=y_filt,
                                    label =  f'{self.description}-{self.channel_name} - filt: {filt_type}'
                                    )


# Function needed from WT_NoiseChannelProc objects to apply a butterworth
def apply_filter(ds:np.ndarray, fs_Hz:float, fc_Hz = 100, filt_order = 2 ):
                 # filter cutoff frequency
    sos = signal.butter(filt_order , fc_Hz, 'lp', fs=fs_Hz, output='sos')
    filtered = signal.sosfilt(sos, ds-ds[0])+ds[0]
    return filtered


# Comparison between power specrtal dencity plots for testing butterworth and 
# FIR approach.

plot_spect_comb2([df_tdms_i1_w0.calc_spectrum(),
                df_tdms_i1_w0.filter(fc_Hz=2_000, filter_func=apply_filter).calc_spectrum(),
                Fir_filter(df_tdms_i1_w0).get_spect_fir_output(fc_hz=0.0002)    ],
                title='CA ws 0 inv 1',
                Kolmogorov_offset=1e3,
                xlim=[1e1,1e5],
                )
#%%
plot_spect_comb2([df_tdms_i1_w5.calc_spectrum(),
                df_tdms_i1_w5.filter(fc_Hz=2_000, filter_func=apply_filter).calc_spectrum(),
                Fir_filter(df_tdms_i1_w5).get_spect_fir_output(fc_hz=0.0002)  ],
                title='CA ws 5 inv 1',
                Kolmogorov_offset=1e3,
                xlim=[1e1,1e5],
                )

plot_spect_comb2([df_tdms_i1_w10.calc_spectrum(),
                df_tdms_i1_w10.filter(fc_Hz=2_000, filter_func= apply_filter).calc_spectrum(),
                Fir_filter(df_tdms_i1_w10).get_spect_fir_output(fc_hz=0.0002)  ],
                title='CA ws 11 inv 1',
                Kolmogorov_offset=1e3,
                xlim=[1e1,1e5],
                )
#%%
