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
    """Construct an object for handling frequency domain plots of raw data."""

    def __init__(self, signal, title):
        """Initialize the object to manage the raw data in frequency domain."""
        self.Title = title
        self.sr = signal.fs_Hz
        self.sig = signal.data
        self.ind = np.array(range(0, len(signal.data_as_Series), 1))
        self.dt = 1 / int(self.sr)
        self.time_sec = self.ind * self.dt

    def fft_calc_and_plot(self, **kwargs):
        """Calculate the fourier transform of a given signal and plot.

        By default we plot the signal in the time domain with the FFT
        representation in a tight layout (in one figure sharing scale).
        """
        n = len(self.time_sec)
        fhat = np.fft.fft(self.sig, n)                      # compute fft
        PSD = fhat * np.conj(fhat) / n                  # Power spectrum (p/f)
        freq = (1/(self.dt*n)) * np.arange(n)           # create x-axis (freq)
        L = np.arange(1, np.floor(n/2), dtype=int)      # plot only first half

        fig, axs = plt.subplots(2, 1,
                                figsize=kwargs.get('figsize',
                                                   None))

        plt.sca(axs[0])
        plt.grid(True, which='both')
        plt.title(self.Title)
        plt.xlabel('Time [s]')
        plt.ylabel('Amplitute (Voltage)')
        plt.plot(self.time_sec, self.sig)
        # plt.loglog(freq[L],(PSD[L]))

        plt.sca(axs[1])
        plt.loglog(freq[L], abs(PSD[L]))
        plt.title('Frequency domain')
        plt.xlabel('Frequencies [Hz]')
        plt.ylabel('Power/Freq')
        plt.grid(True, which='both')

        plt.show()


FFT_new(dfi_i1_w0.decimate(dec=5, offset=0),
        title='Decimation number 5 CA INV ON').fft_calc_and_plot(
            figsize=(12, 9))
len(dfi_i1_w0.decimate(dec=5, offset=0).data)

FFT_new(dfi_i1_w0,
        title='Decimation number 1 INV INV ON').fft_calc_and_plot(
            figsize=(12, 9))
len(dfi_i1_w0.data)

