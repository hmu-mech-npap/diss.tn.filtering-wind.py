#%% [markdown]
# the aim of this file is to investigate the effect of the 
# averaging over decimated and filtered data.
# 
# i.e.: if the signal is recorded at f_r = 100 Hz by averaging all the data over 
#     $dt_r = \frac{1} {f_r}$ period would there be any observable differences for the 
#     a signal obtained at 100 kHZ, 50 KHz or 5 kHz? 
# 
#   Also, will filtering have an effect?
#
# so the idea is:
# - record a signal at a high rate (e.g. 100kHz)
# - For each decimation factor, decimate  the signal as required:
#       - apply a filter on the signal  (if required)
#       - split into  time periods of $dt_r$ duration and average the data
#       - Then at the end perform a power spectrum calculation 
# - plot the power spectrums with different decimation factors
# 
#%%
from pathlib import Path
from matplotlib import pyplot as plt
import scipy.signal as signal
import numpy as np
import pandas as pd

from nptdms import TdmsFile

from pros_noisefiltering.gen_functions import spect,  plot_spect_comb2
from pros_noisefiltering.Graph_data_container import  Graph_data_container
from pros_noisefiltering.WT_NoiProc import WT_NoiseChannelProc, filt_butter_factory, plot_comparative_response
filter_Butter_200=filt_butter_factory(filt_order = 2, fc_Hz = 100)


import logging
logging.basicConfig( level=logging.WARNING)

#%%[markdown]
#
# only the 100 kHz signal is required.  
#
#%%

# I use the current working directory of the file to store the folder with the data for ease (FIR_LP_filter/).
FOLDER_FOR_DATA = Path.cwd()/'measurements_12_05_22'
if not FOLDER_FOR_DATA.exists():   
    FOLDER_FOR_DATA = Path('D:/_data/WEL/WEL20220512/')


#%% [markdown]
#------------------------------------------------------------------
# # Averaging comparison for Compressed air dataset.
# The above procedure should be applied to files with 
# inverter on and off 
#     and 
# WS different than 0


# %%

#Constant directories and names for the .tdms file structure
comp_air_dir = FOLDER_FOR_DATA/ 'compressed air'

TDMS_FNAME = 'Data.tdms'
GROUP_NAME = 'Wind Measurement'
CHAN_NAME = 'Wind2'

# Dir names for the Compressed air measurment

data_CA_inv_0_WS_0 = 'ca0_0.1'
data_CA_inv_0_WS_5 = 'ca0_5.1'
data_CA_inv_0_WS_11= 'ca0_10.1'
data_CA_inv_1_WS_0 = 'ca1_0.1' 
data_CA_inv_1_WS_5 = 'ca1_5.1'
data_CA_inv_1_WS_10= 'ca1_10.1'

path_comp = FOLDER_FOR_DATA / comp_air_dir

# CA stands for compressed air

raw_signal_CA = [data_CA_inv_0_WS_0, data_CA_inv_0_WS_5, 
                data_CA_inv_0_WS_11, data_CA_inv_1_WS_0,
                data_CA_inv_1_WS_5, data_CA_inv_1_WS_10 ]

tdms_raw_CA = []

for item in raw_signal_CA:
    y = f'{path_comp}/{item}'
    x=TdmsFile( Path( y , TDMS_FNAME))
    tdms_raw_CA.append(x)

#%%
# GROUP_NAME = 'Wind Measurement'
# CHAN_NAME = 'Wind 2'

ca_0_0 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[0][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter off, WS=0')
ca_0_5 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[1][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter off, WS=5')
ca_0_10 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[2][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter off, WS=10')
ca_1_0 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[3][GROUP_NAME][CHAN_NAME]
                 , desc= 'Inverter on, WS=0')
ca_1_5 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[4][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter on, WS=5')
ca_1_10 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[5][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter on, WS=10')

#%%
#TODO consider renaming df_tdms_0_0 to df_tdms_i0_w0
# where i: inverter state
# where w: wind speed

#%%
# Estimate the power spectral density of the raw signal
# Hotwire speed 0 m/s
NPERSEG=1024<<8
fc_Hz=200
fr_HZ = 100
#%%
plot_spect_comb2([ca_0_5.calc_spectrum(nperseg=NPERSEG),
                ca_0_5.decimate(10).calc_spectrum(nperseg=NPERSEG/10),
                ca_0_5.decimate(100).calc_spectrum(nperseg=NPERSEG/100)], 
                title='Comparison of spectra for signals at WS=5 for inverter Off \n decimated ',
                xlim =[1e1,3e5], ylim= [1e-7,1e-1],
                markersize=20,
                Kolmogorov_offset=1e0,
                figsize = (15,10), 
                fname=None)

#%%
plot_spect_comb2([ca_0_5.decimate(10).calc_spectrum(nperseg=NPERSEG*100, scaling='density'),
                ca_0_5.decimate(10).calc_spectrum(nperseg=NPERSEG*10, scaling='density'),                
                ca_0_5.decimate(10).calc_spectrum(nperseg=NPERSEG*1, scaling='density')], 
                title='Comparison of spectra for signals at WS=5 for inverter Off \n decimated ',
                xlim =[1e1,3e5], ylim= [1e-7,1e-1],
                markersize=5,
                Kolmogorov_offset=1e0,
                figsize = (15,10), 
                fname=None)



#%%
plot_spect_comb2([ca_0_5.average(fr_Hz=fr_HZ).calc_spectrum(nperseg=NPERSEG/4),
                ca_0_5.decimate(10).average(fr_Hz=fr_HZ).calc_spectrum(nperseg=NPERSEG/4),
                ca_0_5.decimate(100).average(fr_Hz=fr_HZ).calc_spectrum(nperseg=NPERSEG/4)
                ], 
                title='Comparison of spectra for signals at WS=5 for inverter Off \n decimated  and averaged',
                xlim =[1e1,1e2], ylim= [1e-4,1e-1],
                markersize=20,
                Kolmogorov_offset=1e0, 
                fname=None)

#%%
plot_spect_comb2([ca_0_5.filter(fc_Hz=fc_Hz).average(fr_Hz=fr_HZ).set_desc('fr: 100Hz').calc_spectrum(nperseg=NPERSEG/4),
                ca_0_5.decimate(2).filter(fc_Hz=fc_Hz, desc = 'dec=2, fc:100').average(fr_Hz=fr_HZ).set_desc('dec=2, fr: 100Hz').calc_spectrum(nperseg=NPERSEG/4),
                ca_0_5.decimate(20).filter(fc_Hz=fc_Hz,desc = 'dec=20, fc:100').average(fr_Hz=fr_HZ).set_desc('dec=20, fr: 100Hz').calc_spectrum(nperseg=NPERSEG/4)], 
                title='Comparison of spectra for signals at WS=5 for inverter Off \n decimated, filtered and finally averaged ',
                xlim =[1e0,3e2], ylim= [1e-5,1e-0],
                markersize=20,
                Kolmogorov_offset=1e0, 
                fname=None)


# %% [markdown]
# plotting Inverter on measurements at WS 5 m/s
# 
# %%  ===========================================================

NPERSEG=1024
plot_spect_comb2([ca_1_5.calc_spectrum(nperseg=NPERSEG*100),
                ca_1_5.decimate(10).calc_spectrum(nperseg=NPERSEG*10),
                ca_1_5.decimate(100).calc_spectrum(nperseg=NPERSEG)], 
                title='Comparison of spectra for signals at WS=5 for inverter On \n decimated ',
                xlim =[1e1,3e5], ylim= [1e-5,1e-1],
                Kolmogorov_offset=1e0, to_disk=True)
# %%

plot_spect_comb2([ca_1_5.average(fr_Hz=fr_HZ).calc_spectrum(nperseg=NPERSEG/4),
                ca_1_5.decimate(2).average(fr_Hz=fr_HZ).calc_spectrum(nperseg=NPERSEG/4),
                ca_1_5.decimate(20).average(fr_Hz=fr_HZ).calc_spectrum(nperseg=NPERSEG/4)], 
                title='Comparison of spectra for signals at WS=5 for inverter On \n decimated  and averaged',
                xlim =[1e0,3e2], ylim= [1e-4,1e-1],
                markersize=20,
                Kolmogorov_offset=1e0, 
                fname=None)
#%%
fc_Hz = 10
plot_spect_comb2([ca_1_5.filter(fc_Hz=fc_Hz).average(fr_Hz=fr_HZ).calc_spectrum(nperseg=NPERSEG/4),
                ca_1_5.decimate(2).filter(fc_Hz=fc_Hz, desc = 'dec.f:2, fc:100').average(fr_Hz=fr_HZ).calc_spectrum(nperseg=NPERSEG/4),
                ca_1_5.decimate(20).filter(fc_Hz=fc_Hz,desc = 'dec.f:20, fc:100').average(fr_Hz=fr_HZ).calc_spectrum(nperseg=NPERSEG/4)], 
                title='Comparison of spectra for signals at WS=5 for inverter On \n decimated, filtered and finally averaged ',
                xlim =[1e0,3e2], ylim= [1e-7,6e-1],
                markersize=20,
                Kolmogorov_offset=1e-1, 
                fname=None)
# %%



filter_Butter_20 = filt_butter_factory(filt_order =2, fc_Hz = 20)
filter_Butter_200 = filt_butter_factory(filt_order = 2, fc_Hz = 200)
filter_Butter_2000 = filt_butter_factory(filt_order = 2, fc_Hz = 2000)


# %% [markdown] ===========================================================================================================
# # Plots for Presentation 
# Inverter is OFF
# different cut off frequencies.
#%% 
FIGSIZE_SQR = (6,6)
plot_comparative_response(ca_0_10, # cutoff frequency
        filter_func=filter_Butter_20, 
        response_offset=2e-4,            
        Kolmogorov_offset = 4e0,
        nperseg=NPERSEG*100
        ,figsize =FIGSIZE_SQR
        )
plt.savefig('_temp_fig/s3-PS-WS10-filt20')

plot_comparative_response(ca_0_10, # cutoff frequency
        filter_func=filter_Butter_2000, 
        response_offset=2e-4,            
        Kolmogorov_offset = 4e0,
        nperseg=NPERSEG*100
        ,figsize =FIGSIZE_SQR
        )
plt.savefig('_temp_fig/s3-PS-WS10-filt2000')

#%%
plot_comparative_response(ca_0_10, # cutoff frequency
        filter_func=filter_Butter_200, 
        response_offset=2e-4,            
        Kolmogorov_offset = 4e0,
        nperseg=NPERSEG*100
        ,figsize =(12,6)
        )
plt.savefig('_temp_fig/s3-PS-WS10-filt200')

#%%[mardkowng]
# this is for showing the adverse effects of increasing the order usign a 6th order butteworth 
#%%
FIGSIZE_SQR = (6,6)
plot_comparative_response(ca_0_10, # cutoff frequency
        filter_func= filt_butter_factory(filt_order = 6, fc_Hz = 200), 
        response_offset=2e-4,            
        Kolmogorov_offset = 4e0,
        nperseg=NPERSEG*100
        ,figsize =(12,6)
        )
plt.savefig('_temp_fig/s3-PS-WS10-filt20_6')



# %% [markdown]
# ## Cut off frequency 200 Hz - Inverter is ON
plot_comparative_response(ca_1_10, # cutoff frequency
        filter_func=filter_Butter_200, 
        response_offset=2e-4,            
        Kolmogorov_offset = 4e0,
        nperseg=NPERSEG*100
        ,figsize =(12,6)
        )
plt.savefig('_temp_fig/s3-PS-WS10_i1-filt200')





# %% [markdown]
# ## Cut off frequency 200 Hz - Inverter is OFF
# %%
plot_comparative_response(ca_0_0, # cutoff frequency
        filter_func=filter_Butter_200, 
        response_offset=2e-4,
        Kolmogorov_offset = 4e-2,
        nperseg=NPERSEG*100
        ,figsize =(12,8),
        plot_th=False)
plt.savefig(f'_temp_fig/s2-PS-WS0-filt{filter_Butter_200.params.get("fc_Hz")}')
#%%
plot_comparative_response(ca_0_5, # cutoff frequency
        filter_func=filter_Butter_200, 
        response_offset=2e-4,
        Kolmogorov_offset = 1e-0
        ,figsize =FIGSIZE_SQR
        , nperseg=NPERSEG*100
        ,plot_th=False)
plt.savefig(f'_temp_fig/s2-PS-WS5-filt{filter_Butter_200.params.get("fc_Hz")}')

# %%
plot_comparative_response(ca_0_10, # cutoff frequency
        filter_func=filter_Butter_200, 
        response_offset=2e-4,            
        Kolmogorov_offset = 4e0,
        nperseg=NPERSEG*100
        ,figsize =(12,8))
plt.savefig(f'_temp_fig/s2-PS-WS10-filt{filter_Butter_200.params.get("fc_Hz")}')
# %%
    


# %%
# %% [markdown]
# ## Cut off frequency 2000 Hz - Inverter is OFF

plot_comparative_response(ca_0_10, # cutoff frequency
        filter_func=filter_Butter_2000, 
        response_offset=2e-4,            
        Kolmogorov_offset = 4e0,
        nperseg=NPERSEG*100
        ,figsize =(12,8))
plt.savefig(f'_temp_fig/s2-PS-WS10-filt{filter_Butter_2000.params.get("fc_Hz")}')

# %% [markdown]  ==========================================================================================
# # Inverter is On
# ## Cut off frequency 20 Hz - Inverter is On
# %%
plot_comparative_response(ca_1_10, # cutoff frequency
        filter_func=filter_Butter_20, 
        response_offset=2e-4,            
        Kolmogorov_offset = 4e0,
        nperseg=NPERSEG*100
        ,figsize =(12,8))
plt.savefig('_temp_fig/s2-PS-i1-WS10-filt20')
# %%
# ## Cut off frequency 200 Hz - Inverter is On
# %%
plot_comparative_response(ca_1_10, # cutoff frequency
        filter_func=filter_Butter_200, 
        response_offset=2e-4,            
        Kolmogorov_offset = 4e0,
        nperseg=NPERSEG*100
        ,figsize =(12,8))
plt.savefig('_temp_fig/s2-PS-i1-WS10-filt200')

# %% [markdown]
# ## Cut off frequency 2000 Hz - Inverter is On
# %%
plot_comparative_response(ca_1_10, # cutoff frequency
        filter_func=filter_Butter_2000, 
        response_offset=2e-4,            
        Kolmogorov_offset = 4e0,
        nperseg=NPERSEG*100
        ,figsize =(12,8))
plt.savefig('_temp_fig/s2-PS-i1-WS10-filt2000')

# %% [markdown] ===========================================================================================================
# TODO split this into another file
# # Effect of cut off frequency at different wind speeds
# This section is after the "optimal" frequency was selected to test whether there was a difference at different wind speeds


# %%
NPERSEG=1024
plot_comparative_response(ca_0_0, # cutoff frequency
        filter_func=filter_Butter_200, 
        response_offset=2e-4,            
        Kolmogorov_offset = 4e0,
        nperseg=NPERSEG*100
        ,figsize =(12,8))
plt.savefig(f'_temp_fig/s4-PS-WS00-filt{filter_Butter_200.params.get("fc_Hz")}',facecolor='white', transparent=False)

plot_comparative_response(ca_0_5, # cutoff frequency
        filter_func=filter_Butter_200, 
        response_offset=2e-4,            
        Kolmogorov_offset = 4e0,
        nperseg=NPERSEG*100
        ,figsize =(12,8))
plt.savefig(f'_temp_fig/s4-PS-WS05-filt{filter_Butter_200.params.get("fc_Hz")}',facecolor='white', transparent=False)

#%%
plot_comparative_response(ca_0_10, # cutoff frequency
        filter_func=filter_Butter_200, 
        response_offset=2e-4,            
        Kolmogorov_offset = 4e0,
        nperseg=NPERSEG*100
        ,figsize =(12,8))
plt.savefig(f'_temp_fig/s4-PS-WS10-filt{filter_Butter_200.params.get("fc_Hz")}',facecolor='white', transparent=False)



# %%
