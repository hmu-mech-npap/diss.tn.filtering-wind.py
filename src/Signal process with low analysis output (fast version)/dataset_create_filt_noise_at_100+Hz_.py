#%%

import numpy as np
import pandas as pd
from scipy import signal

#Read and store the .h5 file with pandas
f_1 = pd.HDFStore(path='/home/goodvibrations/Documents/Git_clones_dissertation/DSP_Filters_Python-/src/data_folder/noise_reference_raw.h5', mode='r')

data_raw = f_1['/df']


#Store the measurment in one dimentional array and transform it in numpy ndarray for processing 

first_column =data_raw.get('raw-2021.08.31-12:26:54')
sig_inverter_con_off = np.array(first_column)

first_column.info()


second_column = data_raw.get('raw-2021.08.31-12:28:24')
sig_inverter_con_on = np.array(second_column)


third_column = data_raw.get('raw-2021.08.31-12:32:08')
sig_inverter_con_on_WS_5 = np.array(third_column)


fourth_column = data_raw.get('raw-2021.08.31-12:34:29')
sig_inverter_discon_off = np.array(fourth_column)


fifth_column = data_raw.get('raw-2021.08.31-12:35:42')
sig_inverter_discon_on = np.array(fifth_column)


sixth_column = data_raw.get('raw-2021.08.31-12:37:45')
sig_inverter_discon_on_WS_5 = np.array(sixth_column)

#////////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////
#The only filter with les standard deviation on output from input
#Somehow should test more of these kind of filters with no window functions 

#FIR Low-pass filter on the signal with the inverter connected and off

#The length of the filter(number of coefficients, the filter order + 1)
numtaps_2 = 2000
fs = 500000
cutoff_hz = 0.00001
nyq_rate = fs/2 


#Use of firwin to create low-pass FIR filter
fir_co = signal.firwin(numtaps_2, cutoff_hz)
w_fir_co, h_fir_co = signal.freqz(fir_co, [1])



#Apply the filter to the signal column by column from the data set

blank_lp_fir_con_off = signal.lfilter(fir_co, 1.0, sig_inverter_con_off)

blank_lp_fir_con_on = signal.lfilter(fir_co, 1.0, sig_inverter_con_on)

blank_lp_fir_con_on_WS_5 = signal.lfilter(fir_co, 1.0, sig_inverter_con_on_WS_5)

blank_lp_fir_discon_off = signal.lfilter(fir_co, 1.0, sig_inverter_discon_off)

blank_lp_fir_discon_on = signal.lfilter(fir_co, 1.0, sig_inverter_discon_on)

blank_lp_fir_discon_on_WS_5 = signal.lfilter(fir_co, 1.0, sig_inverter_discon_on_WS_5)


#=====================================================
#++++++++ Plot original and filtered signal+++++++++++ 
#=====================================================

#Time interval of the samples
time = np.linspace(0, 7.599998, 3800000)

#The first N-1 samples are corrupted by the initial conditions
warmup = numtaps_2 - 1

#The phase delay of the filtered signal
delay= (warmup / 2) / fs

time_no_shift = time[warmup:]-delay


filt_con_off  = blank_lp_fir_con_off[warmup:]

filt_con_on = blank_lp_fir_con_on[warmup:]

filt_con_on_WS_5 = blank_lp_fir_con_on_WS_5[warmup:]

filt_discon_off = blank_lp_fir_discon_off[warmup:]

filt_discon_on = blank_lp_fir_discon_on[warmup:]

filt_discon_on_WS_5 = blank_lp_fir_discon_on_WS_5[warmup:]

#%%
import h5py

with h5py.File ('/home/goodvibrations/Documents/Git_clones_dissertation/DSP_Filters_Python-/src/data_folder/noise_reference_filt_nt_.h5', 'w') as hdf:
    hdf.create_dataset('filtered Connected and off', data=filt_con_off)
    hdf.create_dataset('filtered Connected and on', data=filt_con_on)
    hdf.create_dataset('filtered Connected on and WS', data=filt_con_on_WS_5)
    hdf.create_dataset('filtered Disconnected and off', data=filt_discon_off)
    hdf.create_dataset('filtered Disconnected and on', data=filt_discon_on)
    hdf.create_dataset('filtered Disconnected on and WS', data=filt_discon_on_WS_5)


# %%
with h5py.File('/home/goodvibrations/Documents/Git_clones_dissertation/DSP_Filters_Python-/src/data_folder/noise_reference_filt_nt_.h5', 'r') as hdf:
    ls = list(hdf.keys())
    sp =list (hdf.head())
    print ('List of datasets in this file: \n', ls)
# %%
