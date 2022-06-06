# Example of pytest for functions
from re import X
import pytest
from functions import (Axis_titles, Fft_Plot_info, 
                        data_import)

from m_CA_Torque_fir import Fir_filter

def test_first_():
    pass

@pytest.fixture
def example_ax_titles() ->Axis_titles:
# Edge case 
# (should not take intergers but the Axis titles class will plot them as titles)
    return Axis_titles(x_title= 5, y_title=7)
    

def test_init_func(example_ax_titles):
    assert example_ax_titles.x_title == 5
    assert example_ax_titles.y_title == 7 

@pytest.fixture
def example_fft_informations()-> Fft_Plot_info: 
    return(Fft_Plot_info(Title=['1','2','1'],filter_type='FIR', signal_state='processed'))

def test_fft_info_init_func(example_fft_informations):
    # Use case
    # information constructor for frequency domain plots
    assert example_fft_informations.title == ['1','2','1']
    assert example_fft_informations.filt_type == 'FIR'
    assert example_fft_informations.sig_state == 'processed'

def test_fft_info_change(example_fft_informations):
    # Test for possibility of editing the information of fft plot
    # after a resulted conclusion for the signal (corrupted from some process)
    assert example_fft_informations.filt_type.replace ('FIR', "butter")
    assert example_fft_informations.sig_state.replace ('processed', 'corrupted')


@pytest.fixture
def ex_data_import()-> data_import:
    file_path = '/mnt/data_folder/'
    file_name = 'noise_reference_'
    file_type = '.h5'
    signal_process = 'raw'

    file_name_h5 = f'{file_name}{signal_process}{file_type}'
    return(data_import(file_path=f'{file_path}',file_name_of_raw=file_name_h5))

def test_f_string_import(ex_data_import):
    # test the new folder path for the data folder
    list1, list2, list3,f_path, f_name = ex_data_import
    assert type(list1)==list
    assert type(list2)==list
    assert type(list3)==list

    assert f_path == '/mnt/data_folder/'
    assert f_name == 'noise_reference_raw.h5'

    


