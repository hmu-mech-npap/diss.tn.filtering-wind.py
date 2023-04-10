#!/usr/bin/env python3
"""Testing the decimate custom function."""
from scipy import signal
import matplotlib.pyplot as plt

from pathlib import Path
from nptdms import TdmsFile

from pros_noisefiltering.WT_NoiProc import (WT_NoiseChannelProc,
                                            Graph_data_container)
from pros_noisefiltering.gen_functions import plot_spect_comb2

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

ca_meas_dir = FOLDER_FOR_DATA / 'compressed air'

data_CA_inv_1_WS_0 = 'ca1_0.1'
# contains the following channels
# [<TdmsChannel with path /'Wind Measurement'/'Torque'>,
#  <TdmsChannel with path /'Wind Measurement'/'Drag'>,
#  <TdmsChannel with path /'Wind Measurement'/'Wind1'>,
#  <TdmsChannel with path /'Wind Measurement'/'Wind2'>]

path_ca_meas = ca_meas_dir / f'{data_CA_inv_1_WS_0}' / TDMS_FNAME

tdms_raw_WT = TdmsFile(path_ca_meas)

ca1_0 = WT_NoiseChannelProc.from_tdms(tdms_raw_WT[GROUP_NAME][CHAN_NAME],
                                      desc='Inverter On, WS=0, 500kHz')
# %%


# Decimation folder measurments
dec_meas_dir = FOLDER_FOR_DATA / 'Decimation'
dec_at_50_kHz = 'de50.1'
dec_at_5_kHz = 'de5.1'
path_dec_meas_50_kHz = dec_meas_dir / f'{dec_at_50_kHz}' / TDMS_FNAME

path_dec_meas_5_kHz = FOLDER_FOR_DATA / dec_meas_dir / f'{dec_at_5_kHz}' / TDMS_FNAME

tdms_raw_WT_50kHz = TdmsFile(path_dec_meas_50_kHz)
tdms_raw_WT_5kHz = TdmsFile(path_dec_meas_5_kHz)


dec_50kHz = WT_NoiseChannelProc.from_tdms(
    tdms_raw_WT_50kHz[GROUP_NAME][CHAN_NAME],
    desc='Inverter On, WS=0, 50kHz')
dec_5kHz = WT_NoiseChannelProc.from_tdms(
    tdms_raw_WT_5kHz[GROUP_NAME][CHAN_NAME],
    desc='Inverter On, WS=0, 5kHz')

NPERSEG = 1024 << 6
FIGSIZE = (15, 10)
medec = 100

print(f"custom decim length: {len(ca1_0.decimate(dec=medec, offset=0).data)}")
y = signal.decimate(ca1_0.data, medec, ftype='fir')
z, f = signal.welch(y,
                    fs=ca1_0.fs_hz/medec,
                    window='flattop',
                    nperseg=NPERSEG/medec,
                    scaling='density')
print(f"decimate with scipy lenght: {len(y)}")
sign = Graph_data_container(_x=z,
                            _y=f,
                            label="dec=100, antialiasing=fir")

plot_spect_comb2([
    ca1_0.decimate(dec=1, offset=0)
    .set_desc('500 kHz origin')
    .calc_spectrum(nperseg=NPERSEG, scaling='density'),

    ca1_0.decimate(dec=medec, offset=0)
    .set_desc('5 kHz (dec=100)')
    .calc_spectrum(nperseg=NPERSEG/medec, scaling='density'),

    dec_5kHz.set_desc('5 kHz origin')
    .calc_spectrum(nperseg=NPERSEG/100, scaling='density')],

                 title='Our custom decimation without antialiasing filter',
                 xlim=[1e0, 1e6], ylim=[1e-5, 0.5e-2],
                 figsize=FIGSIZE,
                 draw_lines=True
                 )
plot_spect_comb2([
    ca1_0.decimate(dec=1, offset=0)
    .set_desc('500 kHz origin')
    .calc_spectrum(nperseg=NPERSEG, scaling='density'),

    sign,
    dec_5kHz.set_desc('5 kHz origin')
    .calc_spectrum(nperseg=NPERSEG/100, scaling='density')],
                 title="Scipy's signal.decimate with antialiasing filter",
                 xlim=[1e0, 1e6], ylim=[1e-5, 0.5e-2],
                 figsize=FIGSIZE,
                 draw_lines=True
                 )
plt.show()
