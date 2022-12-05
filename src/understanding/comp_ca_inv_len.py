"""Comparison of compressed air measurements with wind tunnel."""

from pathlib import Path
from matplotlib import pyplot as plt
from scipy import signal
import numpy as np
from nptdms import TdmsFile
from numpy.fft import fft
from pros_noisefiltering.WT_NoiProc import WT_NoiseChannelProc


def apply_filter(data_sig: np.ndarray, fs_hz: float, fc_hz=100, filt_order=2):
    """# Applying IIR filter.

    This function lets the user apply a butterworth IIR filter and
    get the filtered signal as a result.
    """
    # filter cutoff frequency
    sos = signal.butter(filt_order, fc_hz, 'lp', fs=fs_hz, output='sos')
    filtered = signal.sosfilt(sos, data_sig-data_sig[0])+data_sig[0]
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

l_tdms_CA = []

for item in raw_signal_CA:
    x = TdmsFile(Path(f'{path_comp}/{item}', TDMS_FNAME))
    l_tdms_CA.append(x)

# %%
# [print(x) for x in l_tdms_CA[0][GROUP_NAME].channels()]

GROUP_NAME = 'Wind Measurement'
CHAN_NAME = 'Wind2'


df_tdms_0_0 = WT_NoiseChannelProc.from_tdms(
    l_tdms_CA[0][GROUP_NAME][CHAN_NAME], desc='Inverter off, WS=0')

df_tdms_0_5 = WT_NoiseChannelProc.from_tdms(
    l_tdms_CA[1][GROUP_NAME][CHAN_NAME], desc='Inverter off, WS=5')

df_tdms_0_10 = WT_NoiseChannelProc.from_tdms(
    l_tdms_CA[2][GROUP_NAME][CHAN_NAME], desc='Inverter off, WS=11')

df_tdms_1_0 = WT_NoiseChannelProc.from_tdms(
    l_tdms_CA[3][GROUP_NAME][CHAN_NAME], desc='Inverter on, WS=0')

df_tdms_1_5 = WT_NoiseChannelProc.from_tdms(
    l_tdms_CA[4][GROUP_NAME][CHAN_NAME], desc='Inverter on, WS=5')

df_tdms_1_10 = WT_NoiseChannelProc.from_tdms(
    l_tdms_CA[5][GROUP_NAME][CHAN_NAME], desc='Inverter on, WS=10')


INV_MEAS_DIR = 'inverter'
# Inverter measurements of interest
DATA_INV_INV_0_WS_0 = 'in0_0.1'
DATA_INV_INV_1_WS_0 = 'in1_0.1'
DATA_INV_INV_1_WS_5 = 'in1_5.1'
DATA_INV_INV_1_WS10 = 'in1_10.1'
DATA_INV_INV_1_WS15 = 'in1_15.1'
DATA_INV_INV_1_WS_20 = 'in1_20.1'


path_comp = FOLDER_FOR_DATA / INV_MEAS_DIR

# suffixes:
# - CA : compressed air
# - Inv : Inverter
# - DEC : decimation

raw_signal_CA = [DATA_INV_INV_0_WS_0, DATA_INV_INV_1_WS_0,
                 DATA_INV_INV_1_WS_5, DATA_INV_INV_1_WS10,
                 DATA_INV_INV_1_WS15, DATA_INV_INV_1_WS_20]

l_tdms_Inv = []

for item in raw_signal_CA:
    x = TdmsFile(Path(f'{path_comp}/{item}', TDMS_FNAME))
    l_tdms_Inv.append(x)

# %%
# [print(x) for x in l_tdms_Inv[0][GROUP_NAME].channels()]
# %%
dfi_i0_w0 = WT_NoiseChannelProc.from_tdms(
    l_tdms_Inv[0][GROUP_NAME][CHAN_NAME], desc='Inverter Off, WS=0, 100kHz')
dfi_i1_w0 = WT_NoiseChannelProc.from_tdms(
    l_tdms_Inv[1][GROUP_NAME][CHAN_NAME], desc='Inverter On, WS=0, 100kHz')
dfi_i1_w5 = WT_NoiseChannelProc.from_tdms(
    l_tdms_Inv[2][GROUP_NAME][CHAN_NAME], desc='Inverter On, WS=5, 100kHz')
dfi_i1_w10 = WT_NoiseChannelProc.from_tdms(
    l_tdms_Inv[3][GROUP_NAME][CHAN_NAME], desc='Inverter On, WS=10, 100kHz')
dfi_i1_w15 = WT_NoiseChannelProc.from_tdms(
    l_tdms_Inv[4][GROUP_NAME][CHAN_NAME], desc='Inverter On, WS=15, 100kHz')
dfi_i1_w20 = WT_NoiseChannelProc.from_tdms(
    l_tdms_Inv[5][GROUP_NAME][CHAN_NAME], desc='Inverter On, WS=20, 100kHz')


# print(f' {len(df_tdms_1_0.data_as_Series)/len(dfi_i1_w0.data_as_Series)})
# print(f'{len(df_tdms_1_0.data_as_Series)}\n{len(dfi_i1_w0.data_as_Series)}')


class FftNew:
    """# Better approach to fft.

    Here is an example of how the calculation of fft for a given
    signal is implemented.

    Examples
    ----------
    >>> def fft_calc_and_plot(self):
    >>>    n = len(self.time_sec)
    >>>    # compute fft
    >>>    fhat = np.fft(self.sig, n)
    >>>    # Power spectrum (power/freq)
    >>>    PSD = fhat * np.conj(fhat) / n
    >>>    # create x-axis (frequencies)
    >>>    freq = (1/(self.dt*n)) * np.arange(n)
    >>>    # plot only first half (possitive)
    >>>    plt_pos = np.arange(1, np.floor(n/2), dtype=int)

    Reference
    ----------
    http://databookuw.com/
    """

    def __init__(self, sign, title):
        """# Object initialize.

        This function constructs an object for a given signal
        which will be plotted in the frequency domain.
        """
        self.plt_title = title
        self.samp_rate = sign.fs_Hz
        self.sig = sign.data
        self.ind = sign.data_as_Series.index
        self.time_interv = 1 / int(self.samp_rate)
        self.time_sec = self.ind * self.time_interv

    def fft_calc_and_plot(self):
        """# FFT calculation and plotting.

        This function is used to calculate and plot a signal in the
        frequency domain using the fft library from numpy.
        """
        num_samp = len(self.time_sec)
        # compute fft
        fhat = fft(self.sig, num_samp)
        # Power spectrum (power/freq)
        psd = fhat * np.conj(fhat) / num_samp
        # create x-axis (frequencies)
        freq = (1/(self.time_interv * num_samp)) * np.arange(num_samp)
        # plot only first half (possitive)
        plt_pos = np.arange(1, np.floor(num_samp/2), dtype=int)

        fig, axs = plt.subplots(2, 1)

        plt.sca(axs[0])
        plt.grid(True, which='both')
        plt.title(self.plt_title)
        plt.xlabel('Time [s]')
        plt.ylabel('Amplitute (Voltage)')
        plt.plot(self.time_sec, self.sig)
        # plt.loglog(freq[plt_pos],(PSD[plt_pos]))

        plt.sca(axs[1])
        plt.loglog(freq[plt_pos], abs(psd[plt_pos]))
        plt.title('Frequency domain')
        plt.xlabel('Frequencies [Hz]')
        plt.ylabel('Power/Freq')
        plt.grid(True, which='both')


FftNew(df_tdms_1_0.decimate(dec=5, offset=0),
       title='Decimation number 5 CA INV ON').fft_calc_and_plot()

len(df_tdms_1_0.decimate(dec=5, offset=0).data)

FftNew(dfi_i1_w0, title='Decimation number 1 INV INV ON').fft_calc_and_plot()
len(dfi_i1_w0.data)

FftNew(df_tdms_1_0, title='Decimation None CA INV ON').fft_calc_and_plot()
len(df_tdms_1_0.data)
# This addition is for the inferior python shell
# for plotting the graphs using gtk app
plt.show()

x = FftNew(df_tdms_1_5, title="None")
print(x.time_sec)

# # Here I test the differencies among Welch's method and the new algorithm
# # for power spectral density estimation

# # Inverter state 0
# print(f' {np.std(df_tdms_0_0.data)}')

# print(f' \n {np.std(dfi_i0_w0.data)}')

# # Inverter state 1
# print(f' : \n {np.std(df_tdms_1_0.data)}')

# print(f'ON] : \n {np.std(dfi_i1_w0.data)}')

# # Inverter state 1 WS 5
# print(f'WS:5]] : \n {np.std(df_tdms_1_5.data)}')

# print(f'ON[WS:5]] : \n {np.std(dfi_i1_w5.data)}')

# # Inverter state 1 WS 10
# print(f'WS:10]] : \n {np.std(df_tdms_1_10.data)}')

# print(f'ON[WS:10]] : \n {np.std(dfi_i1_w10.data)}')
