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
import matplotlib
import scipy.signal as signal
import numpy as np
import pandas as pd

import nptdms
from nptdms import TdmsFile

from functions import spect, plot_spect_comb2, Graph_data_container
from signal_process_plots_datasets.FIR_LP_filter.decim_Torque import WT_Noise_ChannelProcessor

#%% Imported from raw_signal_Comp2


#%% Functions and classes
def apply_filter(ds:np.ndarray, fs_Hz:float, fc_Hz = 100, filt_order = 2 ):
                 # filter cutoff frequency
    sos = signal.butter(filt_order , fc_Hz, 'lp', fs=fs_Hz, output='sos')
    filtered = signal.sosfilt(sos, ds-ds[0])+ds[0]
    return filtered



class WT_Noise_ChannelProcessor_averaging():
    #TODO Consider using class methods to implement factory methods. (from tdms or ) 
    def __init__(self, tdms_channel:nptdms.tdms.TdmsChannel, desc:str) -> None:
        """_summary_

        Args:
            tdms_channel (nptdms.tdms.TdmsChannel): tmds channel 
            desc (str): descirption (used)
        """        
        self._channel_data= tdms_channel
        self.set_description(desc=desc)
        # process details
        self.fs_Hz = 1/self._channel_data.properties['wf_increment']
        self.data = self._channel_data.data
        self.channel_name = self._channel_data.name
        self.group_name = self._channel_data.group_name
            
    def set_description(self, desc):
        self.description = desc
        
    def raw_data(self):
        """returns the raw data as a pd.Series

        Returns:
            _type_: _description_
        """        
        return pd.Series(self.data, name=f'{self.channel_name}:raw')
    
    def get_decimated(self, dec:int, offset:int) -> dict:
        """returns a decimated data seires

        Args:
            dec (int): decimation factor
            offset (int): initial offset 

        Returns:
            _type_: a decimated data series. 
        """        
        decimated_fs_Hz = self.fs_Hz/dec
        
        return {fs_Hz:decimated_fs_Hz, 'data': self.data[offset::dec]}
    
    def filter(self, fc_Hz:float, fs_Hz:None):
        """performs 

        Args:
            fc_Hz (float): cutoff frequency in Hz
            fs_Hz (float): sampling frequency in Hz

        Returns:
            _type_: _description_
        """        
        fs_Hz = fs_Hz if fs_Hz is not None else self.fs_Hz
        filtered = apply_filter(ds=self.data, fs_Hz=fs_Hz, fc_Hz=fc_Hz )
        return pd.Series(filtered, name=f'{self.channel_name}:filt_fc_{fc_Hz}')
    
    def get_spectrum_raw(self)->Graph_data_container:
        """returns a Graph_data_container object with the power spectrum of the data. 

        Returns:
            _type_: _description_
        """        
        x_r,y_r = spect(self.data, FS=self.fs_Hz)        
        return Graph_data_container(x=x_r,y = y_r, label = f'{self.description}-{self.channel_name}')
    
    
    def get_spectrum_raw_dec(self, dec:int, offset:int=0)->Graph_data_container:
        """returns a Graph_data_container object with the power spectrum of the **decimated** data. 

        Args:
            dec (int): decimation factor 
            offset (int, optional): offset. Defaults to 0.

        Returns:
            Graph_data_container: _description_
        """        
        decimated_fs_Hz = self.fs_Hz/dec
        x_r,y_r = spect(self.data[offset::dec], FS=decimated_fs_Hz)        
        return Graph_data_container(x=x_r,y = y_r, 
            label = f'{self.description}-{self.channel_name}-fs:{decimated_fs_Hz/1000:.1f}kHz ')
    
    
    def get_spectrum_filt(self, fc_Hz:float)->Graph_data_container:
        """returns a Graph_data_container object with the power spectrum of the data. 

        Args:
            fc_Hz (float): _description_

        Returns:
            Graph_data_container: _description_
        """        
        x_f,y_f = spect(self.filter(fc_Hz=fc_Hz), FS=self.fs_Hz)        
        return Graph_data_container(x=x_f,y = y_f, label = f'{self.description}-{self.channel_name} - filt: {fc_Hz}')
    
    def plot_filtered_th(self,fc_Hz):
        plt.plot(self.data, label = 'raw')
        plt.plot(self.filter(fc_Hz=fc_Hz), label = f'filtered: {fc_Hz}')

    def get_averaged(self, fr_Hz:100):
        """returns 

        Args:
            fr_Hz (100): recording frequency (with averaging)
        """        
        ds = self.raw_data()
        fs_Hz = self.fs_Hz
        fr_Hz = 100
    
        ds_fr = ds.groupby(ds.index// (fs_Hz/fr_Hz)).mean()
        #TODO use factory method to return a new object. 
        return ds 
    
    @classmethod
    def from_tdms(cls, tdms_channel:nptdms.tdms.TdmsChannel, desc:str):
        """Factory methor that generates an object class
        #TOD need to change the init function and test. 

        Args:
            tdms_channel (nptdms.tdms.TdmsChannel): tmds channel 
            desc (str): descirption (used)
        """        
        _channel_data= tdms_channel
        desc

        fs_Hz = 1/_channel_data.properties['wf_increment']
        data = _channel_data.data
        channel_name =_channel_data.name
        group_name = _channel_data.group_name
        return cls(desc, fs_Hz, data, channel_name, group_name, _channel_data)
#%%[markdown]
#
# only the 100 kHz signal is required.  
#
#%%

# I use the current working directory of the file to store the folder with the data for ease (FIR_LP_filter/).
#FOLDER_FOR_DATA = Path.cwd()
# FOLDER_FOR_DATA = Path.cwd()/'measurements_12_05_22'
FOLDER_FOR_DATA = Path('D:/_data/WEL/WEL20220512/')

#%%

#Constant directories and names for the .tdms file structure
tdms_f_name = 'Data.tdms'
tdms_folder_id = 'WTmeas20220512-'

#%% [markdown]


GROUP_NAME = 'Wind Measurement'
CHAN_NAME = 'Torque'

#%%
# Inverter measurments 
# Dir name 
inv_meas_dir = 'Inverter'

WT_inv_1_WS_0 = '115754'
# contains the following channels
# [<TdmsChannel with path /'Wind Measurement'/'Torque'>,
#  <TdmsChannel with path /'Wind Measurement'/'Drag'>,
#  <TdmsChannel with path /'Wind Measurement'/'Wind1'>,
#  <TdmsChannel with path /'Wind Measurement'/'Wind2'>]

path_inv_meas = FOLDER_FOR_DATA / inv_meas_dir / f'{tdms_folder_id}{WT_inv_1_WS_0}' / tdms_f_name

tdms_raw_WT =TdmsFile(path_inv_meas)

df_tdms_inv_meas_1_0 = WT_Noise_ChannelProcessor_averaging(tdms_raw_WT[GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter On, WS=0, 100kHz')
#%%


# Decimation folder measurments 
dec_meas_dir = 'Decimation'
dec_at_50_kHz = '121419'
dec_at_5_kHz = '121435'
path_dec_meas_50_kHz = FOLDER_FOR_DATA / dec_meas_dir / f'{tdms_folder_id}{dec_at_50_kHz}' / tdms_f_name

path_dec_meas_5_kHz = FOLDER_FOR_DATA / dec_meas_dir / f'{tdms_folder_id}{dec_at_5_kHz}' / tdms_f_name

tdms_raw_WT_50kHz =TdmsFile(path_dec_meas_50_kHz)
tdms_raw_WT_5kHz =TdmsFile(path_dec_meas_5_kHz)


df_tdms_dec_50kHz = WT_Noise_ChannelProcessor_averaging(tdms_raw_WT_50kHz[GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter On, WS=0, 50kHz')
df_tdms_dec_5kHz = WT_Noise_ChannelProcessor_averaging(tdms_raw_WT_5kHz[GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter On, WS=0, 5kHz')

# %%
%matplotlib qt
ds = df_tdms_inv_meas_1_0.raw_data()
ds = df_tdms_inv_meas_1_0.
fs_Hz = df_tdms_inv_meas_1_0.fs_Hz
fr_Hz = 100

ds_100 = ds.groupby(ds.index// (fs_Hz/fr_Hz)).mean()

plt.plot(ds.index/fs_Hz, ds, '.', alpha = 0.3)
plt.plot(ds_100.index/fr_Hz, ds_100, '.', alpha = 1)

# %%
# %%
# %%
# %%
# %%
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Up to here 
# #%%
# plot_spect_comb2([df_tdms_inv_meas_1_0.get_spectrum_raw_dec(dec=1)],
#                 title='Raw signal at 100kHz',
#                 xlim=[1e1,1e5], ylim = [1e-4,1e-2])
                
# #%%
# # %matplotlib inline
# # %matplotlib qt
# # plot 50 kHz signals
# plot_spect_comb2([df_tdms_inv_meas_1_0.get_spectrum_raw_dec(dec=2, offset=1),
#                   df_tdms_dec_50kHz.get_spectrum_raw_dec(dec=1)
#                   ],
#                 title='Comparison at 50kHz',
#                 xlim=[1e1,1e5], ylim = [1e-4,1e-2])



# #%%
# # plot 5 kHz signals
# plot_spect_comb2([df_tdms_inv_meas_1_0.get_spectrum_raw_dec(dec=20),
#                   df_tdms_dec_50kHz.get_spectrum_raw_dec(dec=10),
#                   df_tdms_dec_5kHz.get_spectrum_raw_dec(dec=1)
#                   ],
#                 title='Comparison at 5kHz',
#                 xlim=[1e1,1e5], ylim = [1e-4,1e-2])


# #%%[markdown]
# # 20220529-2352:
# # the three plots show different behaviour at the 10 Hz region
# # it could be because of the nperseg parameter
# # I should consider:
# # - modifying the **nperseg** parameter accordingly. 
# # - checking out the behavior of 
# # - plotting stacked versions of the plot spectrum for an easier *comparison*. 



#%%
class Plotter_Class():
    #TODO Not Implemented
    """#TODOthis is a class that can take different object
    and takes their raw data and plot:
    - Time histories
    - spectrums 
    """    
    pass