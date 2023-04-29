"""A testing file for new approaches couse i need lsp."""
import logging
from pathlib import Path
from matplotlib import pyplot as plt
import scipy.signal as signal
import numpy as np
import pandas as pd

from nptdms import TdmsFile
# import nptdms

from pros_noisefiltering.WT_NoiProc import (filt_butter_factory,
                                            fir_factory_constructor,
                                            plot_comparative_response)
from pros_noisefiltering.WT_NoiProc import WT_NoiseChannelProc

filter_Butter_200 = filt_butter_factory(filt_order=2, fc_Hz=100)

# from pros_noisefiltering.gen_functions import (Fft_Plot_info,
#                                                Axis_titles,
#                                                plot_FFT,
#                                                Signals_for_fft_plot,
#                                                fft_calc_sig,
#                                                fft_sig)

# from pros_noisefiltering.Graph_data_container import Graph_data_container

# from numpy.fft import fft, ifft

logging.basicConfig(level=logging.WARNING)

NPERSEG = 1024


def apply_filter(sig_r: np.ndarray, fs_hz: float,
                 fc_hz_real=100, filt_order=2):
    """Apply a butterworth default filter that could be mutated later."""
    sos = signal.butter(filt_order, fc_hz_real, 'lp', fs=fs_hz, output='sos')
    filtered = signal.sosfilt(sos, sig_r-sig_r[0])+sig_r[0]
    return filtered


FOLDER_FOR_DATA = Path(
    '/mnt/data_folder/measurements_12_05_22/new_record_prop_channel/')
if not FOLDER_FOR_DATA.exists():
    FOLDER_FOR_DATA = Path('D:/_data/WEL/WEL20220512/')

# %% CONSTANTS
FIGSIZE_STD = (6, 6)
# Constant directories and names for the .tdms file structure
# Dir name
TDMS_FNAME = 'Data.tdms'
GROUP_NAME = 'Wind Measurement'
CHAN_NAME = 'Wind2'

comp_air_dir = 'compressed air'

# %%
# preparing tdms files
# New renamed folders for rec version information
data_CA_inv_0_WS_0 = 'ca0_0.1'
data_CA_inv_0_WS_5 = 'ca0_5.1'
data_CA_inv_0_WS_11 = 'ca0_10.1'
data_CA_inv_1_WS_0 = 'ca1_0.1'
data_CA_inv_1_WS_5 = 'ca1_5.1'
data_CA_inv_1_WS_10 = 'ca1_10.1'

path_comp = FOLDER_FOR_DATA / comp_air_dir

# CA stands for compressed air

raw_signal_CA = [data_CA_inv_0_WS_0, data_CA_inv_0_WS_5,
                 data_CA_inv_0_WS_11, data_CA_inv_1_WS_0,
                 data_CA_inv_1_WS_5, data_CA_inv_1_WS_10]

l_tdms_CA = []

for item in raw_signal_CA:
    x = TdmsFile(Path(f'{path_comp}/{item}', TDMS_FNAME))
    l_tdms_CA.append(x)

# %%
# [print(x) for x in l_tdms_CA[0][GROUP_NAME].channels()]

GROUP_NAME = 'Wind Measurement'
CHAN_NAME = 'Wind2'


df_tdms_0_0 = WT_NoiseChannelProc.from_tdms(
    l_tdms_CA[0][GROUP_NAME][CHAN_NAME],
    desc='Inverter off, WS=0')
df_tdms_0_5 = WT_NoiseChannelProc.from_tdms(
    l_tdms_CA[1][GROUP_NAME][CHAN_NAME],
    desc='Inverter off, WS=5')
df_tdms_0_10 = WT_NoiseChannelProc.from_tdms(
    l_tdms_CA[2][GROUP_NAME][CHAN_NAME],
    desc='Inverter off, WS=11')
df_tdms_1_0 = WT_NoiseChannelProc.from_tdms(
    l_tdms_CA[3][GROUP_NAME][CHAN_NAME],
    desc='Inverter on, WS=0')
df_tdms_1_5 = WT_NoiseChannelProc.from_tdms(
    l_tdms_CA[4][GROUP_NAME][CHAN_NAME],
    desc='Inverter on, WS=5')
df_tdms_1_10 = WT_NoiseChannelProc.from_tdms(
    l_tdms_CA[5][GROUP_NAME][CHAN_NAME],
    desc='Inverter on, WS=10')

inv_meas_dir = 'inverter'
# Inverter measurements of interest
data_inv_inv_0_WS_0 = 'in0_0.1'
data_inv_inv_1_WS_0 = 'in1_0.1'
data_inv_inv_1_WS_5 = 'in1_5.1'
data_inv_inv_1_WS10 = 'in1_10.1'
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
                 data_inv_inv_1_WS_20]

l_tdms_Inv = []

for item in raw_signal_CA:
    x = TdmsFile(Path(f'{path_comp}/{item}', TDMS_FNAME))
    l_tdms_Inv.append(x)

# %%
# [print(x) for x in l_tdms_Inv[0][GROUP_NAME].channels()]
# %%
dfi_i0_w0 = WT_NoiseChannelProc.from_tdms(
    l_tdms_Inv[0][GROUP_NAME][CHAN_NAME],
    desc='Inverter Off, WS=0, 100kHz')
dfi_i1_w0 = WT_NoiseChannelProc.from_tdms(
    l_tdms_Inv[1][GROUP_NAME][CHAN_NAME],
    desc='Inverter On, WS=0, 100kHz')
dfi_i1_w5 = WT_NoiseChannelProc.from_tdms(
    l_tdms_Inv[2][GROUP_NAME][CHAN_NAME],
    desc='Inverter On, WS=5, 100kHz')
dfi_i1_w10 = WT_NoiseChannelProc.from_tdms(
    l_tdms_Inv[3][GROUP_NAME][CHAN_NAME],
    desc='Inverter On, WS=10, 100kHz')
dfi_i1_w15 = WT_NoiseChannelProc.from_tdms(
    l_tdms_Inv[4][GROUP_NAME][CHAN_NAME],
    desc='Inverter On, WS=15, 100kHz')
dfi_i1_w20 = WT_NoiseChannelProc.from_tdms(
    l_tdms_Inv[5][GROUP_NAME][CHAN_NAME],
    desc='Inverter On, WS=20, 100kHz')

filter_fir_default = fir_factory_constructor(fir_order=2, fc_Hz=100)

fc_Hz = 200
fir_or = 65

fir_filter_cnstr_xorder = fir_factory_constructor(fir_order=fir_or,
                                                  fc_Hz=fc_Hz)
FIGSIZE_SQR_L = (8, 10)
plot_comparative_response(df_tdms_1_10,       # cutoff frequency
                          filter_func=fir_filter_cnstr_xorder,
                          response_offset=2e-4,
                          Kolmogorov_offset=4e0,
                          nperseg=NPERSEG*100,
                          # xlim=0e0,
                          figsize=FIGSIZE_SQR_L)

plot_comparative_response(df_tdms_1_10,             # cutoff frequency
                          filter_func=filter_Butter_200,
                          response_offset=2e-4,
                          Kolmogorov_offset=4e0,
                          nperseg=NPERSEG*100,
                          figsize=FIGSIZE_SQR_L)
# plt.savefig(
#     f'_temp_fig/s4-PS-i1-WS05-filt{filter_Butter_200.params.get("fc_Hz")}',
#     facecolor='white',
#     transparent=False)

plt.show()
