"""Here the idea is to compare the lenths of the datasets.

I think there are more samples in the CA dataset than
in the INV dataset recorded in June
"""

from pathlib import Path
from matplotlib import pyplot as plt
import scipy.signal as signal
import numpy as np

from nptdms import TdmsFile

from pros_noisefiltering.WT_NoiProc import WT_NoiseChannelProc

# %% [markdown]
# This file is for comparing the spectrum of a filtered time series
#
#  ### The first 3 plots are a comparison between the signals with
#  the compressed air.
#  - Here the signals are compared with respect of the Inverter state
#       - **on/off**

# %% Functions and classes


def apply_filter(sig_r: np.ndarray, fs_hz: float,
                 fc_hz=100, filt_order=2):
    """Documented from papadaki."""
    sos = signal.butter(filt_order, fc_hz,
                        'lp', fs=fs_hz,
                        output='sos')
    filtered = signal.sosfilt(sos, sig_r-sig_r[0])+sig_r[0]
    return filtered


# %%
# CONSTANTS
# I use the current working directory of the file to store
# the folder with the data for ease (FIR_LP_filter/).
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

# %%
# Dir names for the Compressed air measurment
#
# =================================================
#
# Here the Compressed air measurements are imported
#
# =================================================
#
comp_air_dir = 'compressed air'

# %% preparing tdms files
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
# %%
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

#
# =================================================
#
# Here the Inverter measurements are imported
#
# =================================================
#
# %%
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


print(f'For each sample in inverter dataset there are \n\
       {len(df_tdms_1_0.data_as_Series)/len(dfi_i1_w0.data_as_Series)} \n\
        samples in CA dataset')

print(f'This should be close :\n length of CA :\n\
        {len(df_tdms_1_0.data_as_Series)} \n and :\n length of inverter:\n\
        {len(dfi_i1_w0.data_as_Series)}')


class FFT_new:
    """This class is used to calculate the fourier transform for raw signal."""

    def __init__(self, signal, title):
        """Construct the appropriate object to manipulate the signal.

        We should be able to integrate this in WT_Noi_proc.
        """
        self.Title = title
        self.sr = signal.fs_hz
        self.sig = signal.data
        self.ind = signal.data_as_Series.index
        self.dt = 1 / int(self.sr)
        self.time_sec = self.ind * self.dt

    def fft_calc_and_plot(self):
        """Func body for calculation of the frequency domain of raw data."""
        n = len(self.time_sec)
        fhat = np.fft.fft(self.sig, n)                  # compute fft
        PSD = fhat * np.conj(fhat) / n                  # Power spectrum (pr/f)
        freq = (1/(self.dt*n)) * np.arange(n)           # create x-axis (freqs)
        L = np.arange(1, np.floor(n/2), dtype=int)      # plot only first half

        fig, axs = plt.subplots(2, 1)

        plt.sca(axs[0])
        plt.grid('both')
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
        plt.grid('both')


FFT_new(df_tdms_1_0.decimate(dec=5, offset=0),
        title='Decimation number 5 CA INV ON').fft_calc_and_plot()
len(df_tdms_1_0.decimate(dec=5, offset=0).data)

FFT_new(dfi_i1_w0, title='Decimation number 1 INV INV ON').fft_calc_and_plot()
len(dfi_i1_w0.data)

FFT_new(df_tdms_1_0, title='Decimation None CA INV ON').fft_calc_and_plot()
len(df_tdms_1_0.data)

# uncomment the line if the plots are not
# showing with the python inferior shell (emacs)
plt.show()

# printing the standard deviation for the 2 sources of measurements

# Inverter state 0
print(
    f'The standard deviation for the CA set is : \n\
    {np.std(df_tdms_0_0.data)}')

print(f'The standard deviation for the Inverter`s set is : \n\
       {np.std(dfi_i0_w0.data)}')

# Inverter state 1
print(f'The standard deviation for the CA set is [ON] : \n\
       {np.std(df_tdms_1_0.data)}')

print(f'The standard deviation for the Inverter`s set is [ON] : \n\
       {np.std(dfi_i1_w0.data)}')

# Inverter state 1 WS 5
print(f'The standard deviation for the CA set is [ON [WS:5]] : \n\
       {np.std(df_tdms_1_5.data)}')

print(f'The standard deviation for the Inverter`s set is [ON[WS:5]] : \n\
       {np.std(dfi_i1_w5.data)}')

# Inverter state 1 WS 10
print(f'The standard deviation for the CA set is [ON [WS:10]] : \n\
       {np.std(df_tdms_1_10.data)}')

print(f'The standard deviation for the Inverter`s set is [ON[WS:10]] : \n\
       {np.std(dfi_i1_w10.data)}')
