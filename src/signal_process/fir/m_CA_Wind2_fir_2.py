import logging

# %%
# Functions and variables to be imported
from pathlib import Path
from nptdms import TdmsFile
import matplotlib.pyplot as plt

from pros_noisefiltering.WT_NoiProc import WT_NoiseChannelProc
from pros_noisefiltering.filters.fir import fir_factory_constructor
from pros_noisefiltering.filters.iir import filt_butter_factory, apply_filter

from pros_noisefiltering.gen_functions import plot_spect_comb2

logging.basicConfig(level=logging.WARNING)
fc_hz = 200

# %%
# This is changed only for me due to format
# I use the current working directory of the file to store
# the folder with the data for ease (FIR_LP_filter/).
FOLDER_FOR_DATA = Path(
    '/mnt/data_folder/measurements_12_05_22/new_record_prop_channel/')
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


NPERSEG = 1024 << 6
fir_2000 = fir_factory_constructor(fir_order=60, fc_Hz=2000)
fir_200 = fir_factory_constructor(fir_order=60, fc_Hz=200)
butter_filter_2000 = filt_butter_factory(filt_order=4, fc_Hz=2000)

# plot_comparative_response(df_tdms_i0_w0,
#                           filter_func=fir_2000,
#                           response_offset=2e-4,
#                           Kolmogorov_offset=4e0,
#                           nperseg=NPERSEG,
#                           figsize=(8, 4))
# # Comparison between power specrtal dencity plots for testing butterworth and
# # FIR approach.
# plot_comparative_response(df_tdms_i1_w0,
#                           filter_func=fir_2000,
#                           response_offset=2e-4,
#                           Kolmogorov_offset=4e0,
#                           nperseg=NPERSEG,
#                           figsize=(8, 4))
plot_spect_comb2([df_tdms_i1_w0.calc_spectrum(),
                  df_tdms_i1_w0
                  .filter(fc_Hz=2_000, filter_func=apply_filter)
                  .calc_spectrum()],
                 # Fir_filter(df_tdms_i1_w0)
                 # .get_spect_fir_output(fc_hz=0.0002)],
                 title='CA ws 0 inv 1',
                 Kolmogorov_offset=1e3,
                 xlim=[1e1, 6e5],
                 ylim=[1e-9, 1e-3]
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
                 xlim=[1e1, 2e5],
                 ylim=[1e-9, 1e-3]
                 )

plot_spect_comb2([df_tdms_i1_w10.calc_spectrum(),
                  df_tdms_i1_w10
                  .filter(fc_Hz=2_000, filter_func=apply_filter)
                  .calc_spectrum()],
                 # Fir_filter(df_tdms_i1_w10)
                 # .get_spect_fir_output(fc_hz=0.0002)],
                 title='CA ws 11 inv 1',
                 Kolmogorov_offset=1e3,
                 xlim=[1e1, 2e5],
                 ylim=[1e-9, 1e-3]
                 )
# # %%
plt.show()
