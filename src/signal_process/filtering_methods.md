# 1.3. Contents of signal_process folder

This folder contains all necessary files for applying varius filters

# iir folder
Here all methods using `IIR` filters and varius signal processing methods, such as:
- decimation
- averaging etc.

# fir folder
Same usage as iir folder but for testing `FIR` filters.

# Test files
## **test_functions.py :**
This file is used to run tests for my functions: 
- I test the fir factory method and assert the initial constructor
- Also test the plotting operation with a dummy signal with `unittest.mock` using `patch` feature which allows for plot testing. 
- Example for plotting functions testing
```python3
from unittest.mock import patch
import pytest

# These functions are for constructing the object and plotting from pypkg
from pros_noisefiltering.WT_NoiProc import (WT_NoiseChannelProc,
                                            Fir_filter,
                                            filt_butter_factory,
                                            fir_factory_constructor,
                                            plot_comparative_response)

@pytest.fixture
def example_wtncp() -> WT_NoiseChannelProc:
    return WT_NoiseChannelProc(desc='description sample', fs_Hz=1000,
                               # +15 seems to originate in bit flip
                               # from 0000 -> 1111 = 15
                               # needed to test the FIR functions with
                               # filtering
                               data=np.linspace(0, 100, 2000+15),
                               channel_name='Torque',
                               group_name='Wind Measurement',
                               _channel_data=None,
                               operations=['New object (init)']
                               )

@pytest.fixture
def fir_wrapper(example_wtncp):
    obj_filt = WT_NoiseChannelProc.from_obj(example_wtncp, operation='copy')
    return (obj_filt)


@patch("matplotlib.pyplot.show")
def test_fir_plots(mock_show, fir_wrapper):
    fc_Hz = 5
    fir_or = 30
    NPERSEG = 1_024
    fir_filter_cnstr_xorder = fir_factory_constructor(fir_order=fir_or,
                                                      fc_Hz=fc_Hz)
    FIGSIZE_SQR_L = (8, 10)
    plot_comparative_response(fir_wrapper,       # cutoff frequency
                              filter_func=fir_filter_cnstr_xorder,
                              response_offset=2e-4,
                              Kolmogorov_offset=4e0,
                              nperseg=NPERSEG,
                              # xlim=0e0,
                              figsize=FIGSIZE_SQR_L)


```

- For now implementation is only for some basic tests and doesn't have proper coverage but could help a lot in the future.

# _archive folder
This folder will contain all deprecated methods and processing techniques until we decide to delete the files permanently from the project.
