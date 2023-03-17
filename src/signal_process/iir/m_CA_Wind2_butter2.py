'''This is a version that uses the new package pros_noisefiltering.'''
# %%
from pathlib import Path
from matplotlib import pyplot as plt
import scipy.signal as signal
import numpy as np
import pandas as pd

from nptdms import TdmsFile
import nptdms


import pros_noisefiltering as pnf 
from pros_noisefiltering.gen_functions import spect,plot_spect_comb2

from pros_noisefiltering.WT_NoiProc import WT_NoiseChannelProc
from pros_noisefiltering.Graph_data_container import Graph_data_container


# %% [markdown]
# This file is for comparing the spectrum of a filtered time series
#
#  ### The first 3 plots are a comparison between the signals
#  with the compressed air.
#  - Here the signals are compared with respect of the Inverter state
#       - **on/off**

# %% Functions and classes
def apply_filter(sig_r: np.ndarray, fs_hz: float, fc_hz=100, filt_order=2):
    """Apply a butterworth filter with sos output."""
    sos = signal.butter(filt_order, fc_hz, 'lp', fs=fs_hz, output='sos')
    filtered = signal.sosfilt(sos, sig_r-sig_r[0])+sig_r[0]
    return filtered


# %%
# CONSTANTS

# Update for automated path detection
FOLDER_FOR_DATA = Path(
    '/home/dtos_experiment/Documents/data_folder')/'measurements_12_05_22/new_record_prop_channel/'
if not FOLDER_FOR_DATA.exists():
    FOLDER_FOR_DATA = Path('D:/_data/WEL/WEL20220512/')

# Constant directories and names for the .tdms file structure
TDMS_FNAME = 'Data.tdms'

# Dir names for the Compressed air measurment
COMP_AIR_DIR = 'compressed air'

# %% preparing tdms files
# New renamed folders for rec version information
DATA_CA_INV_0_WS_0 = 'ca0_0.1'
DATA_CA_INV_0_WS_5 = 'ca0_5.1'
DATA_CA_INV_0_WS_11 = 'ca0_10.1'
DATA_CA_INV_1_WS_0 = 'ca1_0.1'
DATA_CA_INV_1_WS_5 = 'ca1_5.1'
DATA_CA_INV_1_WS_10 = 'ca1_10.1'

path_comp = FOLDER_FOR_DATA / COMP_AIR_DIR

# CA stands for compressed air

raw_signal_CA = [DATA_CA_INV_0_WS_0, DATA_CA_INV_0_WS_5,
                 DATA_CA_INV_0_WS_11, DATA_CA_INV_1_WS_0,
                 DATA_CA_INV_1_WS_5, DATA_CA_INV_1_WS_10]

tdms_raw_CA = []

for item in raw_signal_CA:
    y = f'{path_comp}/{item}'
    x = TdmsFile(Path(y, TDMS_FNAME))
    tdms_raw_CA.append(x)

# %%
GROUP_NAME = 'Wind Measurement'
CHAN_NAME = 'Wind2'


df_tdms_0_0 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[0]
                                            [GROUP_NAME]
                                            [CHAN_NAME],
                                            desc='Inverter off, WS=0')
df_tdms_0_5 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[1]
                                            [GROUP_NAME][CHAN_NAME],
                                            desc='Inverter off, WS=5')
df_tdms_0_10 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[2]
                                             [GROUP_NAME][CHAN_NAME],
                                             desc='Inverter off, WS=11')
df_tdms_1_0 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[3]
                                            [GROUP_NAME][CHAN_NAME],
                                            desc='Inverter on, WS=0')
df_tdms_1_5 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[4]
                                            [GROUP_NAME][CHAN_NAME],
                                            desc='Inverter on, WS=5')
df_tdms_1_10 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[5]
                                             [GROUP_NAME][CHAN_NAME],
                                             desc='Inverter on, WS=10')

# %%
# consider renaming df_tdms_0_0 to df_tdms_i0_w0
# where i: inverter state
# where w: wind speed

# %%
# Estimate the power spectral density of the raw signal
# Hotwire speed 0 m/s

fc_hz = 2000
plot_spect_comb2([df_tdms_0_0.calc_spectrum(),
                  df_tdms_1_0.calc_spectrum(),
                  df_tdms_1_0.filter(fc_hz=fc_hz,
                                     filter_func=apply_filter)
                  .calc_spectrum(), ],
                 title='Comparison between power spectra at WS=0 ',
                 xlim=[1e2, 1e5], ylim=[1e-7, 1e-2],
                 Kolmogorov_offset=1e3, to_disk=True)


# %%

# Estimate the power spectral density of the raw signal
# Hotwire speed 5 m/s

plot_spect_comb2([df_tdms_0_5.calc_spectrum(),
                  df_tdms_1_5.calc_spectrum(),
                  df_tdms_1_5.filter(fc_hz=fc_hz,
                                     filter_func=apply_filter)
                  .calc_spectrum(), ],
                 title='Comparison between power spectra at WS=5 m/s ',
                 xlim=[1e1, 1e5], ylim=[1e-7, 1e-2],
                 Kolmogorov_offset=1e2, to_disk=True)

# %%
# Estimate the power spectral density of the raw signal

# Hotwire speed 10/11 m/s

# plot_spect_comb2([df_tdms_0_10.calc_spectrum(),
#                   df_tdms_1_10.calc_spectrum(),
#                   df_tdms_1_10.filter(fc_hz=fc_hz, filter_func=apply_filter)
#                   .calc_spectrum(), ],
#                  title='Comparison between power spectra at WS=10 m/s ',
#                  xlim=[1e1, 1e5],
#                  Kolmogorov_offset=1e2, to_disk=True)

plt.show()
