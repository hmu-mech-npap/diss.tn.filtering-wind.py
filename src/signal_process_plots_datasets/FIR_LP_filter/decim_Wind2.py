#%%
from pathlib import Path
from matplotlib import pyplot as plt
import scipy.signal as signal
import numpy as np
import pandas as pd

import nptdms
from nptdms import TdmsFile

from functions import spect, plot_spect_comb2, Graph_data_container

#%% Imported from raw_signal_Comp2


#%% Functions and classes
def apply_filter(ds:np.ndarray, fs_Hz:float, fc_Hz = 100, filt_order = 2 ):
                 # filter cutoff frequency
    sos = signal.butter(filt_order , fc_Hz, 'lp', fs=fs_Hz, output='sos')
    filtered = signal.sosfilt(sos, ds-ds[0])+ds[0]
    return filtered



class WT_Noise_ChannelProcessor():
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



#%%[markdown]
#
# ### Here the decimation factor is tested via comparing the decimated measurments in the following manner    
#   - First plot
#       - Original signal sampled at 100 kHz with Inverter **on** and Wind speed 0 m/s
#   - Second plot
#       - Comparison between signals at 50 kHz from the original signal and the measurment at 50 kHz
#   - Third plot
#       - Comparison between signals at 5 kHz from original, 50 kHz and the measurment at 5 kHz
# 


# I use the current working directory of the file to store the folder with the data for ease (FIR_LP_filter/).
#FOLDER_FOR_DATA = Path.cwd()

# FOLDER_FOR_DATA = Path.cwd()/'measurements_12_05_22'
#FOLDER_FOR_DATA = Path('D:/_data/WEL/WEL20220512/')

FOLDER_FOR_DATA = Path('/mnt/data_folder')/'measurements_12_05_22'
if not FOLDER_FOR_DATA.exists():   
    FOLDER_FOR_DATA = Path('D:/_data/WEL/WEL20220512/')

# If you prefear another folder for storing the data use this
# the last line will join the names like a path from the system
#  
# home_folder = Path.home()
# dir_no_1 = 'folder name as a string'
# dir_no_2 = '.....'
# dir_no_3 = '.....' 
# dir_no_4 = '.....'
#
#FOLDER_FOR_DATA = home_folder / dir_no_1 / dir_no_2 / dir_no_3 / dir_no_4 / ..... / .....

#%%

#Constant directories and names for the .tdms file structure
tdms_f_name = 'Data.tdms'
tdms_folder_id = 'WTmeas20220512-'

#%% [markdown]
### Inverter measurments comparison with decimated 
## Inverter measurment with :
#   - Inverter On
#   - Wind tunnel speed 0 m/s
#       - first plot at 100 kHz
#       - second plot at 50 kHz
#       - third plot at 5 kHz 
#   

GROUP_NAME = 'Wind Measurement'
# Old name
# CHAN_NAME = 'Torque'
CHAN_NAME = 'Wind2'

#%%
# Inverter measurments 
# Dir name 
inv_meas_dir = 'Inverter'

# Old file id 
#WT_inv_1_WS_0 = '115754'

# New measurements proper channel
WT_inv_1_WS_0 = 'inv1_0.1'

# contains the following channels
# [<TdmsChannel with path /'Wind Measurement'/'Torque'>,
#  <TdmsChannel with path /'Wind Measurement'/'Drag'>,
#  <TdmsChannel with path /'Wind Measurement'/'Wind1'>,
#  <TdmsChannel with path /'Wind Measurement'/'Wind2'>]

path_inv_meas = FOLDER_FOR_DATA / inv_meas_dir / f'{WT_inv_1_WS_0}' / tdms_f_name

tdms_raw_WT =TdmsFile(path_inv_meas)

df_tdms_inv_meas_1_0 = WT_Noise_ChannelProcessor(tdms_raw_WT[GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter On, WS=0, 100kHz')
#%%


# Decimation folder measurments 
dec_meas_dir = 'Decimation'
# dec_at_50_kHz = '121419'
# dec_at_5_kHz = '121435'

#New folder names
dec_at_50_kHz = 'de50.1'
dec_at_5_kHz = 'de5.1'
path_dec_meas_50_kHz = FOLDER_FOR_DATA / dec_meas_dir / f'{dec_at_50_kHz}' / tdms_f_name

path_dec_meas_5_kHz = FOLDER_FOR_DATA / dec_meas_dir / f'{dec_at_5_kHz}' / tdms_f_name

tdms_raw_WT_50kHz =TdmsFile(path_dec_meas_50_kHz)
tdms_raw_WT_5kHz =TdmsFile(path_dec_meas_5_kHz)


df_tdms_dec_50kHz = WT_Noise_ChannelProcessor(tdms_raw_WT_50kHz[GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter On, WS=0, 50kHz')
df_tdms_dec_5kHz = WT_Noise_ChannelProcessor(tdms_raw_WT_5kHz[GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter On, WS=0, 5kHz')



#%%
plot_spect_comb2([df_tdms_inv_meas_1_0.get_spectrum_raw_dec(dec=1)],
                title='Raw signal at 100kHz',
                xlim=[1e1,1e5], ylim = [1e-4,1e-2])
                
#%%
# %matplotlib inline
# %matplotlib qt
# plot 50 kHz signals
plot_spect_comb2([df_tdms_inv_meas_1_0.get_spectrum_raw_dec(dec=2, offset=1),
                  df_tdms_dec_50kHz.get_spectrum_raw_dec(dec=1)
                  ],
                title='Comparison at 50kHz',
                xlim=[1e1,1e5], ylim = [1e-4,1e-2])



#%%
# plot 5 kHz signals
plot_spect_comb2([df_tdms_inv_meas_1_0.get_spectrum_raw_dec(dec=20),
                  df_tdms_dec_50kHz.get_spectrum_raw_dec(dec=10),
                  df_tdms_dec_5kHz.get_spectrum_raw_dec(dec=1)
                  ],
                title='Comparison at 5kHz',
                xlim=[1e1,1e5], ylim = [1e-4,1e-2])


#%%[markdown]
# 20220529-2352:
# the three plots show different behaviour at the 10 Hz region
# it could be because of the nperseg parameter
# I should consider:
# - modifying the **nperseg** parameter accordingly. 
# - checking out the behavior of 
# - plotting stacked versions of the plot spectrum for an easier *comparison*. 



# %%
