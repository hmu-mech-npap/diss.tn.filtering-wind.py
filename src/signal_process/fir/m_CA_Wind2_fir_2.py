import logging
# %%
# File for looking at FIR filtering options
# TODO this should be updated with new fft
#
# %%
# Functions and variables to be imported
from pathlib import Path
import numpy as np
import pandas as pd
from nptdms import TdmsFile
from scipy import signal
import matplotlib.pyplot as plt
# from func_fir import lp_firwin
# from scipy import signal
# This is bad practice... import the classes and do the stuff properly
# from raw_signal_comp import (df_tdms_0_0, df_tdms_1_0,
#                              df_tdms_0_5, df_tdms_1_5,
#                              df_tdms_0_11, df_tdms_1_10,
#                              f_spect_tdms_CA, Px_x_tdms_CA)
# Old import from functions.py
# from functions import (WT_NoiseChannelProc.from_tdms, Graph_data_container,
#                         plot_signals, spect, plot_spect_comb2)

from pros_noisefiltering.WT_NoiProc import WT_NoiseChannelProc
from pros_noisefiltering.Graph_data_container import Graph_data_container
from pros_noisefiltering.gen_functions import plot_spect_comb2, spect
from pros_noisefiltering.filters import fir

logging.basicConfig(level=logging.WARNING)
fc_hz = 200

# %%
# This is changed only for me due to format
# I use the current working directory of the file to store
# the folder with the data for ease (FIR_LP_filter/).
FOLDER_FOR_DATA = Path(
    '/mnt')/'data_folder/measurements_12_05_22/new_record_prop_channel/'
if not FOLDER_FOR_DATA.exists():
    FOLDER_FOR_DATA = Path(
        'D:/_data/WEL/WEL20220512/')

# Constant directories and names for the .tdms file structure
tdms_folder_id = 'WTmeas20220512-'
tdms_f_name = 'Data.tdms'

# Dir names for the Compressed air measurment
comp_air_dir = 'compressed air'


# New measurements with renamed folders for future rec version information
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
    x = TdmsFile(Path(y, tdms_f_name))
    tdms_raw_CA.append(x)


GROUP_NAME = 'Wind Measurement'
CHAN_NAME = 'Wind2'

# rename the variables to add index of number in the name as you proposed

df_tdms_i0_w0 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[0]
                                              [GROUP_NAME][CHAN_NAME],
                                              desc='Inverter off, WS=0')
df_tdms_i0_w5 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[1]
                                              [GROUP_NAME][CHAN_NAME],
                                              desc='Inverter off, WS=5')
df_tdms_i0_w11 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[2]
                                               [GROUP_NAME][CHAN_NAME],
                                               desc='Inverter off, WS=11')
df_tdms_i1_w0 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[3]
                                              [GROUP_NAME][CHAN_NAME],
                                              desc='Inverter on, WS=0')
df_tdms_i1_w5 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[4]
                                              [GROUP_NAME][CHAN_NAME],
                                              desc='Inverter on, WS=5')
df_tdms_i1_w10 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[5]
                                               [GROUP_NAME][CHAN_NAME],
                                               desc='Inverter on, WS=10')


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

fir_filter_cnstr_xorder = fir_factory_constructor(fir_order=fir_or, fc_Hz=fc_Hz)

# Function needed from WT_NoiseChannelProc objects to apply a butterworth
def apply_filter(ds: np.ndarray, fs_Hz: float, fc_Hz=100, filt_order=2):

    sos = signal.butter(filt_order, fc_hz, 'lp', fs=fs_Hz, output='sos')
    filtered = signal.sosfilt(sos, ds-ds[0])+ds[0]
    return filtered


# Comparison between power specrtal dencity plots for testing butterworth and
# FIR approach.

plot_spect_comb2([df_tdms_i1_w0.calc_spectrum(),
                  df_tdms_i1_w0
                  .filter(fc_Hz=2_000, filter_func=apply_filter)
                  .calc_spectrum()],
                  # Fir_filter(df_tdms_i1_w0)
                  # .get_spect_fir_output(fc_hz=0.0002)],
                 title='CA ws 0 inv 1',
                 Kolmogorov_offset=1e3,
                 xlim=[1e1, 1e5],
                 )
# %%
plot_spect_comb2([df_tdms_i1_w5.calc_spectrum(),
                  df_tdms_i1_w5
                  .filter(fc_Hz=2_000, filter_func=apply_filter)
                  .calc_spectrum()],
                  # Fir_filter(df_tdms_i1_w5)
                  # .get_spect_fir_output(fc_hz=0.0002)],
                 title='CA ws 5 inv 1',
                 Kolmogorov_offset=1e3,
                 xlim=[1e1, 1e5],
                 )

plot_spect_comb2([df_tdms_i1_w10.calc_spectrum(),
                  df_tdms_i1_w10
                  .filter(fc_Hz=2_000, filter_func= apply_filter)
                  .calc_spectrum()],
                  # Fir_filter(df_tdms_i1_w10)
                  # .get_spect_fir_output(fc_hz=0.0002)],
                 title='CA ws 11 inv 1',
                 Kolmogorov_offset=1e3,
                 xlim=[1e1, 1e5],
                 )
# %%
plt.show()
