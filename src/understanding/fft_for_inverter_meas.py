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
def apply_filter(sig_r:np.ndarray, fs_hz:float, fc_hz = 100, filt_order = 2 ):
                 # filter cutoff frequency
    sos = signal.butter(filt_order , fc_hz, 'lp', fs=fs_hz, output='sos')
    filtered = signal.sosfilt(sos, sig_r-sig_r[0])+sig_r[0]
    return filtered

# %%
#CONSTANTS
# I use the current working directory of the file to store the folder with the data for ease (FIR_LP_filter/).
FOLDER_FOR_DATA = Path('/mnt/data_folder/measurements_12_05_22/new_record_prop_channel/')
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

#%%
# TODO Make this in a class with functions so there is no problem with migrating
# this fft algorithm to pypkg and remove duplicate code (redundancy)
# # reference : https://www.youtube.com/watch?v=s2K1JfNR7Sc
#
class FFT_new:
    def __init__(self, signal):
        self.sr = signal.fs_hz
        self.sig = signal.data
        self.ind = signal.data_as_Series.index
        self.dt = 1/ int(self.sr)
        self.time_sec = self.ind * self.dt


    def fft_calc_and_plot(self):
        n= len(self.time_sec)
        fhat = fft(self.sig,n)                 # compute fft
        PSD = fhat * np.conj(fhat) / n               # Power spectrum (power/freq)
        freq = (1/(self.dt*n)) * np.arange(n)             # create x-axis (frequencies)
        L = np.arange(1,np.floor(n/2),dtype=int)     # plot only first half (possitive)

        fig, axs = plt.subplots(2,1)

        plt.sca(axs[0])
        plt.grid('both')
        plt.title('Time domain of raw signal')
        plt.xlabel('Time [s]')
        plt.ylabel('Amplitute (Voltage)')
        plt.plot(self.time_sec ,self.sig)
        #plt.loglog(freq[L],(PSD[L]))

        plt.sca(axs[1])
        plt.loglog(freq[L],abs(PSD[L]))
        plt.title('Frequency domain')
        plt.xlabel('Frequencies [Hz]')
        plt.ylabel('Power/Freq')
        plt.grid('both')
        plt.show()

# Sample usage for plotting
FFT_new(dfi_i0_w0).fft_calc_and_plot()

# =====================================================================================================================
# ============================ THIS SHOULD BE REPLACED WITH THE CLASS ABOVE !!!!!!!!! =================================
# =====================================================================================================================

# #Here a new algorithm is tested but the results are not promissing
# # reference : https://www.youtube.com/watch?v=s2K1JfNR7Sc
# Sr = dfi_i0_w0.fs_hz
# dt = 1 / int(Sr)
# print (f"The time interval of the measurement is:\n{dt}")

# time_s = dfi_i0_w0.data_as_Series.index * dt               #np.arange(0,7,dt)
# print(f"The time array is: \n {time_s}")

# plt.rcParams ['figure.figsize'] =[16,12]
# plt.rcParams.update ({'font.size': 10})

# n= len(time_s)
# fhat = fft(dfi_i0_w0.data,n)                              # compute fft
# PSD = fhat * np.conj(fhat) / n               # Power spectrum (power/freq)
# freq = (1/(dt*n)) * np.arange(n)             # create x-axis (frequencies)
# L = np.arange(1,np.floor(n/2),dtype=int)     # plot only first half (possitive

# fig, axs = plt.subplots(2,1)

# plt.sca(axs[0])
# plt.grid('both')
# plt.title('Time domain of raw signal')
# plt.xlabel('Time [s]')
# plt.ylabel('Amplitute (Voltage)')
# plt.plot(dfi_i0_w0.data_as_Series.index * dt,dfi_i0_w0.data)
# #plt.loglog(freq[L],(PSD[L]))

# plt.sca(axs[1])
# plt.loglog(freq[L],abs(PSD[L]))
# plt.title('Frequency domain')
# plt.xlabel('Frequencies [Hz]')
# plt.ylabel('Power/Freq')
# plt.grid('both')
# #plt.xscale('log')
# #plt.yscale('log')
# print (dfi_i0_w0.data_as_Series, dfi_i0_w0.data)



# #%%
# # Here the 0 ws is plotted with the inverter on
# Sr = dfi_i1_w0.fs_hz
# dt = 1 / int(Sr)
# print (f"The time interval of the measurement is:\n{dt}")

# time_s = dfi_i1_w0.data_as_Series.index * dt               #np.arange(0,7,dt)
# print(f"The time array is: \n {time_s}")

# plt.rcParams ['figure.figsize'] =[16,12]
# plt.rcParams.update ({'font.size': 10})

# n= len(time_s)
# fhat = fft(dfi_i1_w0.data,n)                              # compute fft
# PSD = fhat * np.conj(fhat) / n               # Power spectrum (power/freq)
# freq = (1/(dt*n)) * np.arange(n)             # create x-axis (frequencies)
# L = np.arange(1,np.floor(n/2),dtype=int)     # plot only first half (possitive

# fig, axs = plt.subplots(2,1)

# plt.sca(axs[0])
# plt.grid('both')
# plt.title('Time domain of raw signal')
# plt.xlabel('Time [s]')
# plt.ylabel('Amplitute (Voltage)')
# plt.plot(dfi_i1_w0.data_as_Series.index * dt,dfi_i1_w0.data)
# #plt.loglog(freq[L],(PSD[L]))

# plt.sca(axs[1])
# plt.loglog(freq[L],abs(PSD[L]))
# plt.title('Frequency domain')
# plt.xlabel('Frequencies [Hz]')
# plt.ylabel('Power/Freq')
# plt.grid('both')
# #plt.xscale('log')
# #plt.yscale('log')
# print (dfi_i1_w0.data_as_Series, dfi_i1_w0.data)


# # # here the plots are comparing the raw signals.
# # # First plot is with the inverter state off and on and ws 0
# # f, yin,yout = fft_sig([fft_calc_sig(dfi_i0_w0.data,
# #                                             dfi_i1_w0.data, label="inv on")])

# # # here the inverter is on and the ws is 5, 10 (1st and 2nd graph respectively)
# # f1, yin1,yout1 = fft_sig([fft_calc_sig(dfi_i1_w5.data,
# #                                             dfi_i1_w10.data, label="inv on")])

# # # here the inverter is on and the ws is 15, 20 (1st and 2nd graph respectively)
# # f2, yin2,yout2 = fft_sig([fft_calc_sig(dfi_i1_w15.data,
# #                                             dfi_i1_w20.data, label="inv on")])


# # ws0 = [f,yin,yout]

# # ws5 = [f1,yin1,yout1]

# # ws10 = [f2,yin2,yout2]

# # data_list = [ws0,ws5,ws10]

# # # %%
# # ws_list = ['ws-0','ws-5/10','ws-15/20']
# # for item,descr_sig in zip(data_list,ws_list):
# #     plot_FFT([Signals_for_fft_plot(freq=item[0], sig1=item[1], sig2= item[2]),],

# #          [Fft_Plot_info(Title="Inverter off/on",
# #                        filter_type='',
# #                        signal_state=f'raw-{descr_sig}-on')     ],

# #          [Axis_titles('Frequency [Hz]', 'Amplitute [dB]')    ]
# #                 )


# # plt.show()
