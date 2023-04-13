from unittest.mock import patch
import pytest
from nptdms import TdmsFile
from pros_noisefiltering.WT_NoiProc import (Fir_filter,
                                            WT_NoiseChannelProc)

from pros_noisefiltering.gen_functions import FFT_new
from pathlib import Path

FOLDER_FOR_DATA = Path(
    '/mnt/data_folder/measurements_12_05_22/new_record_prop_channel/')
if not FOLDER_FOR_DATA.exists():
    FOLDER_FOR_DATA = Path('D:/_data/WEL/WEL20220512/')

TDMS_FNAME = 'Data.tdms'
GROUP_NAME = 'Wind Measurement'
CHAN_NAME = 'Wind2'

inv_meas_dir = 'inverter'
# Inverter measurements of interest
data_inv_inv_0_WS_0 = 'in0_0.1'


path_comp = FOLDER_FOR_DATA / inv_meas_dir

raw_signal_CA = [data_inv_inv_0_WS_0]

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


fc_hz = 200


@pytest.fixture
def fir_func() -> Fir_filter:
    filt = Fir_filter(dfi_i0_w0)
    return(filt)


def test_fft_info_init_func(fir_func):
    assert fir_func.channel_name == "Wind2"
    assert len(fir_func.time_int) == len(fir_func.data)
    assert fir_func.description == dfi_i0_w0.description


@pytest.fixture
def fft_func() -> FFT_new:
    return FFT_new(dfi_i0_w0, title=None)


def test_init_fft(fft_func):
    assert len(fft_func.time_sec) == len(dfi_i0_w0.data_as_Series.index *
                                         (1.0 / dfi_i0_w0.fs_Hz))


@patch("matplotlib.pyplot.show")
def test_plot_operation(mock_show):
    FFT_new(dfi_i0_w0, title=None).fft_calc_and_plot()
