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


fc_hz = 200


# This addition is for the inferior python shell
# for plotting the graphs using gtk app

# Define a class for FIR operations like
def fir_factory_constructor(fir_order=32, fc_Hz: float = 200):
    """Mimicing so this is working with Papadakis solution above."""
    def fir_filter(sig_r: np.ndarray,
                   fs_hz: float, fc_hz_real: float = fc_Hz,
                   fir_filt_order=fir_order):

        fir_filt_coeff = signal.firwin(numtaps=fir_filt_order,
                                       fs=fs_hz,
                                       cutoff=fc_hz_real,
                                       # pass_zero=False ,
                                       # scale= True,
                                       )
        # # Hann approach
        # fir_filt_coeff=signal.firwin(fir_order + 1,
        #                              [0, 200/fs_hz],
        #                              fs=fs_hz , window='hann')

        # make output sos type to ensure normal operation
        # this is crusial for elimination of ending ripples see image above
        sos_fir_mode = signal.tf2sos(fir_filt_coeff, 1)
        sos_filt_data = signal.sosfilt(sos_fir_mode, sig_r-sig_r[0])+sig_r[0]
        warmup = fir_filt_order-1
        uncorrupted_output = sos_filt_data[warmup:]
        # filt_sig_time_int = time[warmup:]-((warmup/2)/fs_hz)
        return uncorrupted_output           # uncorr_sos_output

    # Add the parameter attribute for checking filter response
    fir_filter.params = {'filter order': fir_order, 'fc_Hz': fc_Hz}
    return fir_filter


filter_fir_default = fir_factory_constructor(fir_order=2, fc_Hz=100)


class Fir_filter:
    """This class is used to take a signal as a tdms dataframe object.

    (from pypkg funcs)
    """

    def __init__(self, signals) -> None:
        """Initiate object constructor."""
        self.raw = signals.data
        # self.time_int = np.linspace(0, 7, len(self.raw))
        self.description = signals.description
        self._channel_data = signals._channel_data
        self.fs_hz = int(1/signals._channel_data.properties['wf_increment'])
        self.channel_name = signals._channel_data.name
        self.time_int = np.linspace(0,
                                    len(self.raw) / int(self.fs_hz),
                                    len(self.raw))

    def _fir_filter(self, fc_Hz: float = fc_hz,
                    filter_func=filter_fir_default,
                    fs_hz=None) -> pd.Series:
        """#TODO UPDATE DOCSTRING: return a filtered signal based on.

        Args:
            fc_Hz (float): cut off frequency in Hz
            filter_func : filtering function that
                          takes two arguments (sig_r, fs_hz).
                          Defaults to 100, filt_order = 2).
            fs_hz (None): sampling frequency in Hz (is None in declaration)


        Returns:
            _type_: _description_
        """
        if fs_hz is not None:
            logging.warning(
                f'issued {fs_hz} sampling frequency \
                while the default is {self.fs_Hz}')
        fs_hz = fs_hz if fs_hz is not None else self.fs_hz
        filtered = filter_func(sig_r=self.data, fs_hz=fs_hz, fc_Hz=fc_hz)
        return pd.Series(filtered, name=f'{self.channel_name}:filt_fc_{fc_Hz}')

    def fir_nested_filter(self,  fc_Hz: float,
                          filter_func=filter_fir_default, fs_hz=None,
                          desc=None):
        """Construct a Wrapper for applying a filter."""
        sig_r_filt = self._fir_filter(fc_Hz=fc_hz,
                                      filter_func=filter_func,
                                      fs_hz=fs_hz)
        description = (
            desc if desc is not None else self.description + f'_fc:{fc_Hz}')

        return WT_NoiseChannelProc.from_obj(self,
                                            desc=description,
                                            data=sig_r_filt.values,
                                            operation=f'pass filter {fc_Hz}'
                                            )

    # def apply_fir(self, fc_hz, order_for_filter: int):
    #     filtered = fir_nested_filter(self.raw, fs_hz=self.fs_hz, fc_hz=fc_hz)
    #     return pd.Series(filtered,
    #                      name=f'{self.channel_name}:fir_filt_fc_{fc_hz}')


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
plt.savefig(
    f'_temp_fig/s4-PS-i1-WS05-filt{filter_Butter_200.params.get("fc_Hz")}',
    facecolor='white',
    transparent=False)

plt.show()
