from unittest.mock import patch
import pytest
from pros_noisefiltering.WT_NoiProc import (Fir_filter,
                                            WT_NoiseChannelProc)
from pros_noisefiltering.gen_functions import FFT_new
import numpy as np


@pytest.fixture
def example_wtncp() -> WT_NoiseChannelProc:
    return WT_NoiseChannelProc(desc='description sample', fs_Hz=100,
                               data=np.random.normal((100,)),
                               channel_name='Torque',
                               group_name='Wind Measurement',
                               _channel_data=None,
                               operations=['New object (init)']
                               )


@pytest.fixture
def fft_func(example_wtncp) -> Fir_filter:
    new_obj = WT_NoiseChannelProc.from_obj(example_wtncp, operation='copy')
    # filt = FFT_new(new_obj, title=None)
    return(new_obj)


def test_fft_info_init_func(fft_func):
    filt = FFT_new(fft_func, title=None)
    assert filt.sr == 100
    assert len(filt.time_sec) == len(fft_func.data)
    assert fft_func._channel_data is None


@patch("matplotlib.pyplot.show")
def test_plot_operation(mock_show, fft_func):
    FFT_new(fft_func, title=None).fft_calc_and_plot()
