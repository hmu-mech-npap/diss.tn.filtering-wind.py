"""
Here the idea is to compare the Torque channel.

The comparison is in regard to a decimation factor and
we tryied to test if noise from higher frequencies will
corrupt the recorded signal due to maximal 100 kHz sampling
frequency.
"""
import logging
# useful to keep for decimation chapter
# %% [markdown]
# the aim of this file is to investigate the effect of the
# averaging over decimated and filtered data.
#
# i.e.: if the signal is recorded at f_r = 100 Hz by
#      averaging all the data over $dt_r = \frac{1} {f_r}$
#      period would there be any observable differences for the
#      a signal obtained at 100 kHZ, 50 KHz or 5 kHz?
#
#   Also, will filtering have an effect?
#
# so the idea is:
# - record a signal at a high rate (e.g. 100kHz)
# - For each decimation factor, decimate  the signal as required:
#       - apply a filter on the signal  (if required)
#       - split into  time periods of $dt_r$ duration and average the data
#       - Then at the end perform a power spectrum calculation
# - plot the power spectrums with different decimation factors
#
# %%
# Unused imports as of now
from pathlib import Path
# from scipy import signal
from matplotlib import pyplot as plt
# import scipy.signal as signal
# import numpy as np
# import pandas as pd

# import nptdms
from nptdms import TdmsFile

# TODO Using old deprecaded class PROPABLY DELETE
from pros_noisefiltering.gen_functions import plot_spect_comb2
from pros_noisefiltering.filters.iir import filt_butter_factory
from pros_noisefiltering.WT_NoiProc import WT_NoiseChannelProc

from pros_noisefiltering.plotting_funcs import plot_comparative_response

# Constract a butterworth default
filter_Butter_default = filt_butter_factory(filt_order=2, fc_Hz=100)


logging.basicConfig(level=logging.WARNING)

# %% Imported from raw_signal_Comp2

# %%[markdown]
#
# only the 100 kHz signal is required.
#
# %%
# changed for me
# I use the current working directory of the file to store the folder
# with the data for ease (FIR_LP_filter/).
FOLDER_FOR_DATA = Path(
    '/mnt/data_folder/measurements_12_05_22/new_record_prop_channel/')
if not FOLDER_FOR_DATA.exists():
    FOLDER_FOR_DATA = Path('D:/_data/WEL/WEL20220512/')

# %%

# Constant directories and names for the .tdms file structure
tdms_f_name = 'Data.tdms'

# %% [markdown]
# %% CONSTANTS

GROUP_NAME = 'Wind Measurement'
CHAN_NAME = 'Torque'

# %%
# Inverter measurements
# Dir name
inv_meas_dir = FOLDER_FOR_DATA / 'inverter'

WT_inv_1_WS_0 = 'in1_0.1'
# contains the following channels
# [<TdmsChannel with path /'Wind Measurement'/'Torque'>,
#  <TdmsChannel with path /'Wind Measurement'/'Drag'>,
#  <TdmsChannel with path /'Wind Measurement'/'Wind1'>,
#  <TdmsChannel with path /'Wind Measurement'/'Wind2'>]

path_inv_meas = inv_meas_dir / f'{WT_inv_1_WS_0}' / tdms_f_name

tdms_raw_WT = TdmsFile(path_inv_meas)
[print(x) for x in tdms_raw_WT[GROUP_NAME].channels()]


df_tdms_inv_meas_1_0 = WT_NoiseChannelProc.from_tdms(
    tdms_raw_WT
    [GROUP_NAME]
    [CHAN_NAME],
    desc='Inverter On, WS=0, 100kHz')
# %%


# Decimation folder measurments
dec_meas_dir = FOLDER_FOR_DATA / 'Decimation'
dec_at_50_kHz = 'de50.1'
dec_at_5_kHz = 'de5.1'
path_dec_meas_50_kHz = dec_meas_dir / f'{dec_at_50_kHz}' / tdms_f_name

path_dec_meas_5_kHz = dec_meas_dir / f'{dec_at_5_kHz}' / tdms_f_name

tdms_raw_WT_50kHz = TdmsFile(path_dec_meas_50_kHz)
tdms_raw_WT_5kHz = TdmsFile(path_dec_meas_5_kHz)


df_tdms_dec_50kHz = WT_NoiseChannelProc.from_tdms(
    tdms_raw_WT_50kHz
    [GROUP_NAME]
    [CHAN_NAME],
    desc='Inverter On, WS=0, 50kHz')
df_tdms_dec_5kHz = WT_NoiseChannelProc.from_tdms(
    tdms_raw_WT_5kHz
    [GROUP_NAME]
    [CHAN_NAME],
    desc='Inverter On, WS=0, 5kHz')

# %%
# %matplotlib qt
# sig_r = df_tdms_inv_meas_1_0.raw_data()
# fs_hz = df_tdms_inv_meas_1_0.fs_Hz
# fr_Hz = 100

# sig_r_100 = sig_r.groupby(sig_r.index// (fs_hz/fr_Hz)).mean()

# plt.plot(sig_r.index/fs_hz, sig_r, '.', alpha = 0.3)
# plt.plot(sig_r_100.index/fr_Hz, sig_r_100, '.', alpha = 1)

df_tdms_inv_meas_1_0_av100 = df_tdms_inv_meas_1_0.average(100)
print(df_tdms_inv_meas_1_0.operations)
print(df_tdms_inv_meas_1_0_av100.operations)
print(df_tdms_inv_meas_1_0.decimate(1).operations)
print(df_tdms_inv_meas_1_0.decimate(1).average(100).operations)
print(df_tdms_inv_meas_1_0.filter(fc_Hz=100).average(100).operations)
# %%
# should create testing for class
# print(df_tdms_inv_meas_1_0.fs_hz)
# print(df_tdms_inv_meas_1_0.data)
# print(df_tdms_inv_meas_1_0.data_as_Series)
# print(df_tdms_inv_meas_1_0._filter(fc_hz=100))
# print(df_tdms_inv_meas_1_0.get_spectrum_filt(fc_hz=100)) # graph obj
# print(df_tdms_inv_meas_1_0.get_spectrum_raw_dec(dec=1)) # graph obj

print(df_tdms_inv_meas_1_0.decimate(1).operations)
# print(df_tdms_inv_meas_1_0.get_averaged(fr_Hz=100))   #-> Obj
# %%
# %%
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Up to here
# #%%
plot_spect_comb2([df_tdms_inv_meas_1_0
                  .calc_spectrum_gen(dec=1, nperseg=20*1024),
                  df_tdms_inv_meas_1_0
                  .calc_spectrum_gen(dec=2, nperseg=10*1024),
                  df_tdms_inv_meas_1_0
                  .calc_spectrum_gen(dec=20, nperseg=1024)],
                 title='Comparison of decimated signal 100kHz',
                 xlim=[1e1, 1e5], ylim=[1e-4, 1e-0]
                 )
# %% [markdown]
# ## Comparing averaging after decimation
# comparing the signal
# when different filters are applied and averaging occurs
#
#  this is for ws0 so we may need to look at different WS (with and without)
# %%
plot_spect_comb2([df_tdms_inv_meas_1_0
                  .average(fr_Hz=100)
                  .calc_spectrum_gen(dec=1, nperseg=1024),
                  df_tdms_inv_meas_1_0
                  .decimate(dec=2, offset=0)
                  .average(fr_Hz=100)
                  .calc_spectrum_gen(dec=1, nperseg=1024),
                  df_tdms_inv_meas_1_0
                  .decimate(dec=20, offset=0)
                  .average(fr_Hz=100)
                  .calc_spectrum_gen(dec=1, nperseg=1024)
                  ],
                 title='Comparison of decimated and averaged signal at WS0',
                 xlim=[1e0, 1e4], ylim=[1e-8, 1e-2]
                 )

# %% [markdown]
# ## Comparing averaging after filtering
# comparing the signal
# when different filters are applied and averaging occurs
# %%
plot_spect_comb2([df_tdms_inv_meas_1_0
                  .filter(fc_Hz=100)
                  .average(fr_Hz=100)
                  .calc_spectrum_gen(dec=1, nperseg=1024),
                  df_tdms_inv_meas_1_0
                  .filter(fc_Hz=200)
                  .average(fr_Hz=100)
                  .calc_spectrum_gen(dec=1, nperseg=1024),
                  df_tdms_inv_meas_1_0
                  .filter(fc_Hz=2000)
                  .average(fr_Hz=100)
                  .calc_spectrum_gen(dec=1, nperseg=1024)
                  ],
                 title='Comparison of averaging with different filters',
                 xlim=[1e0, 1e4], ylim=[1e-8, 1e-2]
                 )
# %% [markdown]
# The above procedure should be applied to files with
# inverter on and off
#     and
# WS different than 0

# %%
# # %matplotlib inline
# %matplotlib qt

# %% [markdown]
# ------------------------------------------------------------------
# # Averaging comparison for Compressed air dataset.
# The above procedure should be applied to files with
# inverter on and off
#     and
# WS different than 0


# %%
# CONSTANTS


# Constant directories and names for the .tdms file structure
comp_air_dir = FOLDER_FOR_DATA / 'compressed air'

TDMS_FNAME = 'Data.tdms'
GROUP_NAME = 'Wind Measurement'
CHAN_NAME = 'Wind2'

# Dir names for the Compressed air measurment

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

tdms_raw_CA = []

for item in raw_signal_CA:
    y = f'{path_comp}/{item}'
    x = TdmsFile(Path(y, TDMS_FNAME))
    tdms_raw_CA.append(x)

# GROUP_NAME = 'Wind Measurement'
# CHAN_NAME = 'Torque'

df_tdms_0_0 = WT_NoiseChannelProc.from_tdms(
    tdms_raw_CA[0][GROUP_NAME][CHAN_NAME],
    desc='Inverter off, WS=0')
df_tdms_0_5 = WT_NoiseChannelProc.from_tdms(
    tdms_raw_CA[1][GROUP_NAME][CHAN_NAME],
    desc='Inverter off, WS=5')
df_tdms_0_11 = WT_NoiseChannelProc.from_tdms(
    tdms_raw_CA[2][GROUP_NAME][CHAN_NAME],
    desc='Inverter off, WS=11')
df_tdms_1_0 = WT_NoiseChannelProc.from_tdms(
    tdms_raw_CA[3][GROUP_NAME][CHAN_NAME],
    desc='Inverter on, WS=0')
df_tdms_1_5 = WT_NoiseChannelProc.from_tdms(
    tdms_raw_CA[4][GROUP_NAME][CHAN_NAME],
    desc='Inverter on, WS=5')
df_tdms_1_10 = WT_NoiseChannelProc.from_tdms(
    tdms_raw_CA[5][GROUP_NAME][CHAN_NAME],
    desc='Inverter on, WS=10')

# %%
# consider renaming df_tdms_0_0 to df_tdms_i0_w0
# where i: inverter state
# where w: wind speed

# %%
# Estimate the power spectral density of the raw signal
# Hotwire speed 0 m/s
NPERSEG = 1024
fc_hz = 200
fr_HZ = 100
# %%
plot_spect_comb2([df_tdms_0_5.calc_spectrum(nperseg=NPERSEG*20),
                  df_tdms_0_5.decimate(2).calc_spectrum(nperseg=NPERSEG*10),
                  df_tdms_0_5.decimate(20).calc_spectrum(nperseg=NPERSEG)],
                 title='Spectra for signals at WS=5 inv=Off \n dec',
                 xlim=[1e2, 3e5], ylim=[1e-7, 1e-2],
                 Kolmogorov_offset=1e3, to_disk=True)

# %%
plot_spect_comb2([df_tdms_0_5.average(fr_Hz=fr_HZ)
                  .calc_spectrum(nperseg=NPERSEG/4),
                  df_tdms_0_5.decimate(2)
                  .average(fr_Hz=fr_HZ)
                  .calc_spectrum(nperseg=NPERSEG/4),
                  df_tdms_0_5.decimate(20)
                  .average(fr_Hz=fr_HZ)
                  .calc_spectrum(nperseg=NPERSEG/4)],
                 title='Spectra of signals at WS=5 for inv=Off \n (dec. avg.)',
                 xlim=[1e0, 3e2], ylim=[1e-7, 1e-2],
                 Kolmogorov_offset=2e-2, to_disk=True)
# %%
plot_spect_comb2([df_tdms_0_5.filter(fc_Hz=fc_hz)
                  .average(fr_Hz=fr_HZ)
                  .calc_spectrum(nperseg=NPERSEG/4),
                  df_tdms_0_5.decimate(2)
                  .filter(fc_Hz=fc_hz, desc='dec.f:2, fc:100')
                  .average(fr_Hz=fr_HZ)
                  .calc_spectrum(nperseg=NPERSEG/4),
                  df_tdms_0_5.decimate(20)
                  .filter(fc_Hz=fc_hz, desc='dec.f:20, fc:100')
                  .average(fr_Hz=fr_HZ)
                  .calc_spectrum(nperseg=NPERSEG/4)],
                 title='Comparison of spectra for signals at WS=5 inv=Off \n\
                 dec, filt and finally averaged ',
                 xlim=[1e0, 3e2], ylim=[1e-7, 1e-2],
                 Kolmogorov_offset=2e-2, to_disk=True)


# %% [markdown]
# plotting Inverter on measurements at WS 5 m/s
#
# %%  ===========================================================

plot_spect_comb2([df_tdms_1_5.calc_spectrum(nperseg=NPERSEG*20),
                  df_tdms_1_5.decimate(2).calc_spectrum(nperseg=NPERSEG*10),
                  df_tdms_1_5.decimate(20).calc_spectrum(nperseg=NPERSEG)],
                 title='Comparison of spectra for signals at WS=5 \n\
                 for inverter On decimated',
                 xlim=[1e2, 3e5], ylim=[1e-5, 1e-1],
                 Kolmogorov_offset=1e3, to_disk=True)
# %%

plot_spect_comb2([df_tdms_1_5.average(fr_Hz=fr_HZ)
                  .calc_spectrum(nperseg=NPERSEG/4),
                  df_tdms_1_5.decimate(2)
                  .average(fr_Hz=fr_HZ)
                  .calc_spectrum(nperseg=NPERSEG/4),
                  df_tdms_1_5.decimate(20)
                  .average(fr_Hz=fr_HZ)
                  .calc_spectrum(nperseg=NPERSEG/4)],
                 title='Comparison of spectra for signals at WS=5 for \
                 inverter On \n decimated  and averaged',
                 xlim=[1e0, 3e2], ylim=[1e-7, 1e-2],
                 Kolmogorov_offset=2e-2, to_disk=True)
# %%
fc_hz = 10
plot_spect_comb2([df_tdms_1_5.filter(fc_Hz=fc_hz)
                  .average(fr_Hz=fr_HZ)
                  .calc_spectrum(nperseg=NPERSEG/4),
                  df_tdms_1_5.decimate(2)
                  .filter(fc_Hz=fc_hz, desc='dec.f:2, fc:100')
                  .average(fr_Hz=fr_HZ)
                  .calc_spectrum(nperseg=NPERSEG/4),
                  df_tdms_1_5.decimate(20)
                  .filter(fc_Hz=fc_hz, desc='dec.f:20, fc:100')
                  .average(fr_Hz=fr_HZ)
                  .calc_spectrum(nperseg=NPERSEG/4)],
                 title='Averaged filtered spectra on dec. signals WS=5 inv=On',
                 xlim=[1e0, 3e2], ylim=[1e-7, 1e-2],
                 Kolmogorov_offset=2e-2, to_disk=True)
# %%

# %%

filter_Butter_default = filt_butter_factory(filt_order=2, fc_Hz=200)

plot_comparative_response(df_tdms_0_0,    # cutoff frequency
                          filter_func=filter_Butter_default,
                          response_offset=2e-4,
                          Kolmogorov_offset=1e3,
                          figsize=(12, 8),
                          plot_th=False)
# %%
# plot_comparative_response(df_tdms_0_5,  # cutoff frequency
#         filter_func=filter_Butter_default,
#         response_offset=2e-4,
#         Kolmogorov_offset = 1e3
#         ,figsize =(12,8),
#         plot_th=False)
# plt.savefig(f'_temp_fig/_s3_filter_i0_w5_B{filter_Butter_default.params["fc_Hz"]}.png')

plot_comparative_response(df_tdms_1_5,   # cutoff frequency
                          filter_func=filter_Butter_default,
                          response_offset=2e-4,
                          Kolmogorov_offset=1e3,
                          nperseg=NPERSEG*100,
                          figsize=(12, 8),
                          plot_th=False)
plt.savefig(
    f'_temp_fig/_s3_filt_i1_w5_B{filter_Butter_default.params["fc_Hz"]}.png')

# %%
plot_comparative_response(df_tdms_0_11,   # cutoff frequency
                          filter_func=filter_Butter_default,
                          response_offset=2e-4,
                          Kolmogorov_offset=1e3,
                          nperseg=NPERSEG*100,
                          figsize=(12, 8))

# %%
plt.show()
