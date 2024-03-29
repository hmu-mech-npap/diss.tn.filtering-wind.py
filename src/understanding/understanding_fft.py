# %%
from pathlib import Path
from matplotlib import pyplot as plt
import scipy.signal as signal
import numpy as np
import pandas as pd

from nptdms import TdmsFile
import nptdms


import pros_noisefiltering as pnf
from pros_noisefiltering.gen_functions import (spect,plot_spect_comb2,
                                               Fft_Plot_info,Axis_titles,plot_FFT,Signals_for_fft_plot,
                                               fft_calc_sig,fft_sig)

from pros_noisefiltering.WT_NoiProc import WT_NoiseChannelProc
from pros_noisefiltering.Graph_data_container import Graph_data_container

from numpy.fft import fft, ifft

# %% [markdown]
# This file is for comparing the spectrum of a filtered time series
#
#  ### The first 3 plots are a comparison between the signals with the compressed air.
#  - Here the signals are compared with respect of the Inverter state
#       - **on/off**

#%% Functions and classes
def apply_filter(ds:np.ndarray, fs_Hz:float, fc_Hz = 100, filt_order = 2 ):
                 # filter cutoff frequency
    sos = signal.butter(filt_order , fc_Hz, 'lp', fs=fs_Hz, output='sos')
    filtered = signal.sosfilt(sos, ds-ds[0])+ds[0]
    return filtered

# %%
#CONSTANTS

# Update for automated path detection
FOLDER_FOR_DATA = Path(
    '/mnt/data_folder/measurements_12_05_22/new_record_prop_channel/')
if not FOLDER_FOR_DATA.exists():
    FOLDER_FOR_DATA = Path('D:/_data/WEL/WEL20220512/')

#Constant directories and names for the .tdms file structure

TDMS_FNAME = 'Data.tdms'

# Dir names for the Compressed air measurment
comp_air_dir = 'compressed air'

#%% preparing tdms files
# New renamed folders for rec version information
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
    x=TdmsFile( Path( y , TDMS_FNAME))
    tdms_raw_CA.append(x)

#%%
GROUP_NAME = 'Wind Measurement'
CHAN_NAME = 'Wind2'


df_tdms_0_0 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[0][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter off, WS=0')
df_tdms_0_5 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[1][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter off, WS=5')
df_tdms_0_10 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[2][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter off, WS=11')
df_tdms_1_0 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[3][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter on, WS=0')
df_tdms_1_5 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[4][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter on, WS=5')
df_tdms_1_10 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[5][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter on, WS=10')

#%%
#Here a new algorithm is tested but the results are not promissing
# reference : https://www.youtube.com/watch?v=s2K1JfNR7Sc
Sr = df_tdms_0_0.fs_Hz
dt = 1 / int(Sr)
print (f"The time interval of the measurement is:\n{dt}")

time_s = np.arange(0,7,dt)
print(f"The time array is: \n {time_s}")

plt.rcParams ['figure.figsize'] =[16,12]
plt.rcParams.update ({'font.size': 18})

n= len(time_s)
fhat = fft(df_tdms_0_0.data,n)                              # compute fft
PSD = fhat * np.conj(fhat) / n               # Power spectrum (power/freq)
freq = (1/(dt*n)) * np.arange(n)             # create x-axis (frequencies)
L = np.arange(1,np.floor(n/2),dtype=int)     # plot only first half (possitive

print(f"This is the length of the time array and should be = 2_650_000 >< no {n}")
fig, axs = plt.subplots(2,1)

plt.sca(axs[0])
#plt.plot(time_s,df_tdms_0_0.data)
plt.loglog(freq,abs(PSD))

plt.sca(axs[1])
plt.plot(freq[L],abs(PSD[L]))
#plt.xscale('log')
plt.yscale('log')
plt.show()
print (df_tdms_0_0.data_as_Series, df_tdms_0_0.data)

#%%
#Here my black box fft algorithm from the pkg is tested
#the results are more logical than the prev. alg

f, yin,yout = fft_sig([fft_calc_sig(df_tdms_0_0.data,
                                            df_tdms_1_0.data, label="inv off")])
f1, yin1,yout1 = fft_sig([fft_calc_sig(df_tdms_0_5.data,
                                            df_tdms_1_5.data, label="inv off")])

f2, yin2,yout2 = fft_sig([fft_calc_sig(df_tdms_0_10.data,
                                            df_tdms_1_10.data, label="inv off")])

#some lists for fast plotting 3 plots with a for loop
ws0 = [f,yin,yout]

ws5 = [f1,yin1,yout1]

ws10 = [f2,yin2,yout2]

data_list = [ws0,ws5,ws10]

ws_list = ['ws-0','ws-5','ws-10']
for item,descr_sig in zip(data_list,ws_list):
    plot_FFT([Signals_for_fft_plot(freq=item[0], sig1=item[1], sig2= item[2]),],

         [Fft_Plot_info(Title="Inverter off/on",
                       filter_type='',
                       signal_state=f'raw-{descr_sig}-on')     ],

         [Axis_titles('Frequency [Hz]', 'Amplitute [dB]')    ]
                )


