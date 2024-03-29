"""Decimation and downsampling methods.

Here the goal is to examine whether the
downsampling needed for sane runtimes.
"""
# %%
#
from pathlib import Path
from matplotlib import pyplot as plt
from scipy import signal
import numpy as np

from nptdms import TdmsFile

# from functions import spect, plot_spect_comb2, Graph_data_container
from pros_noisefiltering.WT_NoiProc import WT_NoiseChannelProc
from pros_noisefiltering.gen_functions import plot_spect_comb2


# %%[markdown]
#
# ### Here the decimation factor is tested via comparing the
# decimated measurments in the following manner
#   - First plot
#       - Original signal sampled at 100 kHz with Inverter
#       **on** and Wind speed 0 m/s
#   - Second plot
#       - Comparison between signals at 50 kHz from the
#       original signal and the measurment at 50 kHz
#   - Third plot
#       - Comparison between signals at 5 kHz from original,
#       50 kHz and the measurment at 5 kHz
#

FOLDER_FOR_DATA = Path(
    '/mnt/data_folder')/'measurements_12_05_22/new_record_prop_channel/'
if not FOLDER_FOR_DATA.exists():
    FOLDER_FOR_DATA = Path('D:/_data/WEL/WEL20220512/')


# %%

# Constant directories and names for the .tdms file structure
TDMS_F_NAME = 'Data.tdms'
TDMS_FOLDER_ID = 'WTmeas20220512-'

# %% [markdown]
# ## Inverter measurments comparison with decimated
# # Inverter measurment with :
#   - Inverter On
#   - Wind tunnel speed 0 m/s
#       - first plot at 100 kHz
#       - second plot at 50 kHz
#       - third plot at 5 kHz
#

GROUP_NAME = 'Wind Measurement'
# Old name
# CHAN_NAME = 'Torque'
CHAN_NAME = 'Wind2'

# %%
# Inverter measurments
# Dir name
INV_MEAS_DIR = 'inverter'

# Old file id
# WT_inv_1_WS_0 = '115754'

# New measurements proper channel
WT_INV_1_WS_0 = 'in1_0.1'


path_inv_meas = (
    FOLDER_FOR_DATA / INV_MEAS_DIR / f'{WT_INV_1_WS_0}' / TDMS_F_NAME)

tdms_raw_WT = TdmsFile(path_inv_meas)

df_tdms_inv_meas_1_0 = WT_NoiseChannelProc.from_tdms(
    tdms_raw_WT[GROUP_NAME][CHAN_NAME],
    desc='Inverter On, WS=0, 100kHz')
# %%


# Decimation folder measurments
DEC_MEAS_DIR = 'Decimation'
# dec_at_50_kHz = '121419'
# dec_at_5_kHz = '121435'

# New folder names
DEC_AT_50_KHZ = 'de50.1'
DEC_AT_5_KHZ = 'de5.1'
path_dec_meas_50_kHz = (
    FOLDER_FOR_DATA / DEC_MEAS_DIR / f'{DEC_AT_50_KHZ}' / TDMS_F_NAME)

path_dec_meas_5_kHz = (
    FOLDER_FOR_DATA / DEC_MEAS_DIR / f'{DEC_AT_5_KHZ}' / TDMS_F_NAME)

tdms_raw_WT_50kHz = TdmsFile(path_dec_meas_50_kHz)
tdms_raw_WT_5kHz = TdmsFile(path_dec_meas_5_kHz)


df_tdms_dec_50kHz = WT_NoiseChannelProc.from_tdms(
    tdms_raw_WT_50kHz[GROUP_NAME][CHAN_NAME],
    desc='Inverter On, WS=0, 50kHz')
df_tdms_dec_5kHz = WT_NoiseChannelProc.from_tdms(
    tdms_raw_WT_5kHz[GROUP_NAME][CHAN_NAME],
    desc='Inverter On, WS=0, 5kHz')


# Function needed from WT_NoiseChannelProc objects to apply a butterworth
def apply_filter(sig_r: np.ndarray, fs_hz: float, fc_hz=100, filt_order=2):
    """Is defined in pypkg more clearly i thing."""
    # filter cutoff frequency
    sos = signal.butter(filt_order, fc_hz, 'lp', fs=fs_hz, output='sos')
    filtered = signal.sosfilt(sos, sig_r-sig_r[0])+sig_r[0]
    return filtered


# %%
plot_spect_comb2([df_tdms_inv_meas_1_0.decimate(dec=1)
                  .calc_spectrum_gen(nperseg=1024*100)],
                 title='Raw signal at 100kHz',
                 xlim=[1e1, 1e5], ylim=[1e-4, 1e-2])

# %%
# %matplotlib inline
# %matplotlib qt
# plot 50 kHz signals
plot_spect_comb2([df_tdms_inv_meas_1_0
                  .decimate(dec=2, offset=1)
                  .calc_spectrum_gen(nperseg=1024*10),
                  df_tdms_dec_50kHz
                  .decimate(dec=1)
                  .calc_spectrum_gen(nperseg=1024)
                  ],
                 title='Comparison at 50kHz',
                 xlim=[1e1, 1e5], ylim=[1e-4, 1e-2])
# plot 5 kHz signals
plot_spect_comb2([df_tdms_inv_meas_1_0
                  .decimate(dec=20)
                  .calc_spectrum_gen(nperseg=1024),
                  df_tdms_dec_50kHz
                  .decimate(dec=10)
                  .calc_spectrum_gen(nperseg=1024),
                  df_tdms_dec_5kHz
                  .decimate(dec=1)
                  .calc_spectrum_gen(nperseg=1024)
                  ],
                 title='Comparison at 5kHz',
                 Kolmogorov_offset=1e-0,
                 xlim=[1e1, 1e5], ylim=[1e-4, 1e-2])


# %%[markdown]
# 20220529-2352:
# the three plots show different behaviour at the 10 Hz region
# it could be because of the nperseg parameter
# I should consider:
# - modifying the **nperseg** parameter accordingly.
# - checking out the behavior of
# - plotting stacked versions of the plot spectrum for an easier *comparison*.

plt.show()
