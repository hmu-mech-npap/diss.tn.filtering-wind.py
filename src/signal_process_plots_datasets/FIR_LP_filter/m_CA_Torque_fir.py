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

from func_fir import lp_firwin
from scipy import signal
# This is bad practice... import the classes and do the stuff properly
# from raw_signal_comp import df_tdms_0_0, df_tdms_1_0, df_tdms_0_5, df_tdms_1_5, df_tdms_0_11, df_tdms_1_10, f_spect_tdms_CA, Px_x_tdms_CA

from functions import (WT_Noise_ChannelProcessor, Graph_data_container,
                        plot_signals, spect, plot_spect_comb2)
#Constants
FS = 100_000 # Sampling frequency of the signal

# The lines below will be replaced by a better practice. The variables will not be
# imported from raw_signal_comp.py but constructed as needed
#  

#Construct an FIR filter with signal.firwin() function
# filter_coeff, w, h = lp_firwin(numtaps_2=20, FS=FS, cutoff_Hz=0.0001)
# 
# # Filtering of the signal
# fir_lp_filt_0_0 = signal.lfilter(filter_coeff, 1.0, df_tdms_0_0.iloc[:, 1].values)
# fir_lp_filt_1_0 = signal.lfilter(filter_coeff, 1.0, df_tdms_1_0.iloc[:, 1].values)
# fir_lp_filt_0_5 = signal.lfilter(filter_coeff, 1.0, df_tdms_0_5.iloc[:, 1].values)
# fir_lp_filt_1_5 = signal.lfilter(filter_coeff, 1.0, df_tdms_1_5.iloc[:, 1].values)
# fir_lp_filt_0_11 = signal.lfilter(filter_coeff, 1.0, df_tdms_0_11.iloc[:, 1].values)
# fir_lp_filt_1_10 = signal.lfilter(filter_coeff, 1.0, df_tdms_1_10.iloc[:, 1].values)
# 
# # FIR filter delay elimination (reject corrupted signal)
# warmup = 20-1 #numtaps-1 = order-1
# delay = (warmup/2)/FS
# 
# # Comp. air 0 m/s
# x_fir_0_0, y_fir_0_0 = spect(fir_lp_filt_0_0[warmup:], FS)
# x_fir_1_0, y_fir_1_0 = spect(fir_lp_filt_1_0[warmup:], FS)
# 
# # Comp.air 5 m/s
# x_fir_0_5, y_fir_0_5 = spect(fir_lp_filt_0_5[warmup:], FS)
# x_fir_1_5, y_fir_1_5 = spect(fir_lp_filt_1_5[warmup:], FS)
# 
# # Comp.air 11/10 m/s
# x_fir_0_11, y_fir_0_11 = spect(fir_lp_filt_0_11[warmup:], FS)
# x_fir_1_10, y_fir_1_10 = spect(fir_lp_filt_1_10[warmup:], FS)
# 
# # Plot the spectral density of the raw and filtered signal for the same Wind speed 
# # in one graph
# 
# The plot_spect_comb function will be replaced from the new version 
# (plot_spect_comb2). This is to use the same function and not have multiple 
# functions for plotting the signal spectrum
#  
# Inverter Off
# Compressed air 0 m/s
# plot_spect_comb(x1=x_fir_0_0,y1=y_fir_0_0,
#                 x2=f_spect_tdms_CA[0],y2=Px_x_tdms_CA[0],
#                 x3=0,y3=0,
#                 title='Wind speed CA=0 m/s Inverter Off',
#                 slabel1='Filtered FIR',
#                 slabel2='Raw signal',slabel3='',
#                 xlim=[1e1,1e5]
#                 )
# 
# # Compressed air 5 m/s
# plot_spect_comb(x1=x_fir_0_5,y1=y_fir_0_5,
#                 x2=f_spect_tdms_CA[2],y2=Px_x_tdms_CA[2],
#                 x3=0,y3=0,
#                 title='Wind speed CA=5 m/s Inverter Off',
#                 slabel1='Filtered FIR',
#                 slabel2='Raw signal',slabel3='',
#                 xlim=[1e1,1e5]
#                 )
# 
# # Compressed air 11 m/s
# plot_spect_comb(x1=x_fir_0_11,y1=y_fir_0_11,
#                 x2=f_spect_tdms_CA[4],y2=Px_x_tdms_CA[4],
#                 x3=0,y3=0,
#                 title='Wind speed CA=11 m/s Inverter Off',
#                 slabel1='Filtered FIR',
#                 slabel2='Raw signal',slabel3='',
#                 xlim=[1e1,1e5]
#                 )
# 
# # Inverter On
# # Compressed air 0 m/s
# plot_spect_comb(x1=x_fir_1_0,y1=y_fir_1_0,
#                 x2=f_spect_tdms_CA[1],y2=Px_x_tdms_CA[1],
#                 x3=0,y3=0,
#                 title='Wind speed CA=0 m/s Inverter On',
#                 slabel1='Filtered FIR',
#                 slabel2='Raw signal',slabel3='',
#                 xlim=[1e1,1e5]
#                 )
# 
# # Compressed air 5 m/s
# plot_spect_comb(x1=x_fir_1_5,y1=y_fir_1_5,
#                 x2=f_spect_tdms_CA[3],y2=Px_x_tdms_CA[3],
#                 x3=0,y3=0,
#                 title='Wind speed CA=5 m/s Inverter On',
#                 slabel1='Filtered FIR',
#                 slabel2='Raw signal',slabel3='',
#                 xlim=[1e1,1e5]
#                 )
# 
# # Compressed air 10 m/s
# plot_spect_comb(x1=x_fir_1_10,y1=y_fir_1_10,
#                 x2=f_spect_tdms_CA[5],y2=Px_x_tdms_CA[5],
#                 x3=0,y3=0,
#                 title='Wind speed CA=11 m/s Inverter On',
#                 slabel1='Filtered FIR',
#                 slabel2='Raw signal',slabel3='',
#                 xlim=[1e1,1e5]
#                 )
# 
# 

#%%
# I use the current working directory of the file to store the folder with the data for ease (FIR_LP_filter/).
FOLDER_FOR_DATA = Path.cwd()/'measurements_12_05_22'
if not FOLDER_FOR_DATA.exists():   
    FOLDER_FOR_DATA = Path('D:/_data/WEL/WEL20220512/')

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

# rename the variables to add index of number in the name as you proposed

df_tdms_i0_w0 = WT_Noise_ChannelProcessor(tdms_raw_CA[0][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter off, WS=0')
df_tdms_i0_w5 = WT_Noise_ChannelProcessor(tdms_raw_CA[1][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter off, WS=5')
df_tdms_i0_w11 = WT_Noise_ChannelProcessor(tdms_raw_CA[2][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter off, WS=11')
df_tdms_i1_w0 = WT_Noise_ChannelProcessor(tdms_raw_CA[3][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter on, WS=0')
df_tdms_i1_w5 = WT_Noise_ChannelProcessor(tdms_raw_CA[4][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter on, WS=5')
df_tdms_i1_w10 = WT_Noise_ChannelProcessor(tdms_raw_CA[5][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter on, WS=10')



num_samp = 2_500_000
time_int = np.linspace(0,7,num_samp)

def fir_filter(ds:np.ndarray, fs_hz:float, fc_hz = 0.0002, filt_order = 20):
    filt_coeff, w, h = lp_firwin(filt_order,fs_hz,fc_hz)
    filt_data = signal.lfilter(filt_coeff, 1.0, ds)
    warmup = filt_order-1
    uncorrupted_output = filt_data[warmup:]
    filt_sig_time_int = time_int[warmup:]-((warmup/2)/fs_hz)
    
    return uncorrupted_output, filt_sig_time_int

class Fir_filter:
    def __init__(self,signals) -> None:
    
        self.raw = signals.raw_data()
        self.time_int = np.linspace(0, 7, len(self.raw))
        self.description = signals.description
        self._channel_data= signals._channel_data
        self.fs_Hz = int (1/signals._channel_data.properties['wf_increment'])
        self.channel_name = signals._channel_data.name
    
    def apply_fir(self, fc_hz):
        filtered, filt_time_int = fir_filter(self.raw, fs_hz=self.fs_Hz, fc_hz=fc_hz)
        return pd.Series(filtered, name=f'{self.channel_name}:filt_fc_{fc_hz}')
    
    def get_spect_fir_output(self, fc_hz):
        x_filt, y_filt = spect(self.apply_fir(fc_hz=fc_hz), FS= self.fs_Hz)
        filt_type = 'FIR'
        return Graph_data_container(x=x_filt,y=y_filt,
                                    label =  f'{self.description}-{self.channel_name} - filt: {filt_type}'
                                    )


# plot_signals([Time_domain_data_cont(time_int,test_filt_sig.raw, 
#                                     label='Raw signal') ,
#              Time_domain_data_cont(filtered_signal_fir[1] ,filtered_signal_fir[0] , 
#                                     label='FIR output')  ],
#             [Axis_titles('Time [s]', 'Amplitute [dB]')],
#             Title='CA 0 ws 0 inv test',
#             figsize = (10,6)
#             )

plot_spect_comb2([df_tdms_i1_w0.get_spectrum_raw(),
                df_tdms_i1_w0.get_spectrum_filt(fc_Hz=2_000),
                Fir_filter(df_tdms_i1_w0).get_spect_fir_output(fc_hz=0.0002)    ],
                title='CA ws 0 inv 0',
                Kolmogorov_offset=1e3,
                xlim=[1e1,1e5],
                )

plot_spect_comb2([df_tdms_i1_w5.get_spectrum_raw(),
                df_tdms_i1_w5.get_spectrum_filt(fc_Hz=2_000),
                Fir_filter(df_tdms_i1_w5).get_spect_fir_output(fc_hz=0.0002)  ],
                title='CA ws 5 inv 0',
                Kolmogorov_offset=1e3,
                xlim=[1e1,1e5],
                )

plot_spect_comb2([df_tdms_i1_w10.get_spectrum_raw(),
                df_tdms_i1_w10.get_spectrum_filt(fc_Hz=2_000),
                Fir_filter(df_tdms_i1_w10).get_spect_fir_output(fc_hz=0.0002)  ],
                title='CA ws 11 inv 0',
                Kolmogorov_offset=1e3,
                xlim=[1e1,1e5],
                )
#%%
