# %%

from pathlib import Path
from matplotlib import pyplot as plt
import scipy.signal as signal
import numpy as np
import pandas as pd

from nptdms import TdmsFile
import nptdms
from functions import spect, plot_spect_comb2, Graph_data_container


# %% [markdown]
# This file is for comparing the spectrum of a filtered time series
# 
#  ### The first 3 plots are a comparison between the signals with the compressed air.
#  - Here the signals are compared with respect of the Inverter state
#       - **on/off**

#%% Functions and classes
def apply_filter(ds:np.ndarray, fs_Hz:float, fc_Hz = 100, filt_order = 2 ):
                 # filter cutoff frequency
    sos = signal.butter(filt_order , fc_Hz, 'lp', fs=fs_Hz, output='sos')
    filtered = signal.sosfilt(sos, ds-ds[0])+ds[0]
    return filtered



class WT_Noise_ChannelProcessor():
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
    
    def filter(self, fc_Hz:float):
        """performs 

        Args:
            fc_Hz (float): _description_

        Returns:
            _type_: _description_
        """        
        filtered = apply_filter(ds=self.data, fs_Hz=self.fs_Hz, fc_Hz=fc_Hz )
        return pd.Series(filtered, name=f'{self.channel_name}:filt_fc_{fc_Hz}')
    
    def get_spectrum_raw(self):
        x_r,y_r = spect(self.data, FS=self.fs_Hz)        
        return Graph_data_container(x=x_r,y = y_r, label = f'{self.description}-{self.channel_name}')
    
    def get_spectrum_filt(self, fc_Hz:float):
        x_f,y_f = spect(self.filter(fc_Hz=fc_Hz), FS=self.fs_Hz)        
        return Graph_data_container(x=x_f,y = y_f, label = f'{self.description}-{self.channel_name} - filt: {fc_Hz}')
    
    def plot_filtered_th(self,fc_Hz):
        plt.plot(self.data, label = 'raw')
        plt.plot(self.filter(fc_Hz=fc_Hz), label = f'filtered: {fc_Hz}')

# %%
#CONSTANTS

 #  I use the current working directory of the file to store the folder with the data for ease (FIR_LP_filter/).
 # FOLDER_FOR_DATA = Path.cwd()/'measurements_12_05_22'
 # FOLDER_FOR_DATA = Path('D:/_data/WEL/WEL20220512/')

# Update for automated path detection
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


#Constant directories and names for the .tdms file structure
tdms_folder_id = 'WTmeas20220512-'
tdms_f_name = 'Data.tdms'

# Dir names for the Compressed air measurment
comp_air_dir = 'compressed air'

data_CA_inv_0_WS_0 = '112318'
data_CA_inv_0_WS_5 = '112629'
data_CA_inv_0_WS_11= '112709'
data_CA_inv_1_WS_0 = '113005' 
data_CA_inv_1_WS_5 = '113534'
data_CA_inv_1_WS_10= '113614'

path_comp = FOLDER_FOR_DATA / comp_air_dir / tdms_folder_id

# CA stands for compressed air

raw_signal_CA = [data_CA_inv_0_WS_0, data_CA_inv_0_WS_5, 
                data_CA_inv_0_WS_11, data_CA_inv_1_WS_0,
                data_CA_inv_1_WS_5, data_CA_inv_1_WS_10 ]

tdms_raw_CA = []

for item in raw_signal_CA:
    y = f'{path_comp}{item}'
    x=TdmsFile( Path( y , tdms_f_name))
    tdms_raw_CA.append(x)


GROUP_NAME = 'Wind Measurement'
CHAN_NAME = 'Torque'

df_tdms_0_0 = WT_Noise_ChannelProcessor(tdms_raw_CA[0][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter off, WS=0')
df_tdms_0_5 = WT_Noise_ChannelProcessor(tdms_raw_CA[1][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter off, WS=5')
df_tdms_0_11 = WT_Noise_ChannelProcessor(tdms_raw_CA[2][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter off, WS=11')
df_tdms_1_0 = WT_Noise_ChannelProcessor(tdms_raw_CA[3][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter on, WS=0')
df_tdms_1_5 = WT_Noise_ChannelProcessor(tdms_raw_CA[4][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter on, WS=5')
df_tdms_1_10 = WT_Noise_ChannelProcessor(tdms_raw_CA[5][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter on, WS=10')

#%%
#TODO consider renaming df_tdms_0_0 to df_tdms_i0_w0
# where i: inverter state
# where w: wind speed

#%%
# Estimate the power spectral density of the raw signal
# Hotwire speed 0 m/s

fc_Hz=2000
plot_spect_comb2([df_tdms_0_0.get_spectrum_raw(),
                df_tdms_1_0.get_spectrum_raw(),
                df_tdms_1_0.get_spectrum_filt(fc_Hz),], 
                 title='Comparison between power spectra at WS=0 ',
                     xlim =[1e2,1e5], ylim= [1e-7,1e-2],
                Kolmogorov_offset=1e3, to_disk=True)


#%%

# Estimate the power spectral density of the raw signal
# Hotwire speed 5 m/s

plot_spect_comb2([
                df_tdms_0_5.get_spectrum_raw(),
                df_tdms_1_5.get_spectrum_raw(),
                df_tdms_1_5.get_spectrum_filt(fc_Hz=fc_Hz),], 
                title='Comparison between power spectra at WS=5 m/s ',
                xlim =[1e1,1e5], ylim= [1e-7, 1e-2],
                Kolmogorov_offset=1e2, to_disk=True)

#%%
# Estimate the power spectral density of the raw signal

# Hotwire speed 10/11 m/s

plot_spect_comb2([df_tdms_0_11.get_spectrum_raw(),
                df_tdms_1_10.get_spectrum_raw(),
                df_tdms_1_10.get_spectrum_filt(fc_Hz=fc_Hz),], 
                title='Comparison between power spectra at WS=10 m/s ',
                     xlim =[1e1,1e5],
                Kolmogorov_offset=1e2, to_disk=True)


# %%  CODE USed for developing the Class
# ============================================================

# DATASET_NO = 2
# fc_Hz = 100

# # channel_data = tdms_raw_CA[DATASET_NO ]['Wind Measurement']['Torque']

# # fs_Hz= 1/channel_data.properties['wf_increment']
# # # fs_Hz= 1e5

# # ds1 = tdms_raw_CA[DATASET_NO].as_dataframe().iloc[:, 1].values
# # ds1 = channel_data.data 
# # filtered = apply_filter(ds=ds1,fs_Hz=fs_Hz, fc_Hz=fc_Hz )


# # df_tmp = pd.DataFrame({'raw': ds1, 'filt': filtered})
# # # %%
# # x_r,y_r = spect(df_tmp.iloc[:, 0].values, FS=fs_Hz)
# # x_f,y_f = spect(df_tmp.iloc[:, 1].values, FS=fs_Hz)
# # # %%
# # gc_r = Graph_data_container(x=x_r,y = y_r, label = 'raw')
# # gc_f = Graph_data_container(x=x_f,y = y_f, label = df_tmp.iloc[:,1].name)

# # plot_spect_comb2([gc_r, gc_f], title='first attempt to show filter',
# #                      xlim =[1e1,1e5],
# #                 Kolmogorov_offset=1e2, to_disk=True)
# # # %%
# # plot_spect_comb2([gc_r], title='first attempt to show filter',
# #                      xlim =[1e1,1e5],
# #                 Kolmogorov_offset=1e2, to_disk=True)

# # # %%
# # plot_spect_comb2([gc_f], title=f'first attempt to show filter (cutoff: {fc_Hz}Hz)',
# #                      xlim =[1e1,1e5],
# #                 Kolmogorov_offset=5e0, to_disk=True)

# # %%

# #%%
# DATASET_NO = 2
# fc_Hz = 100
# %matplotlib qt
# wt =  WT_Noise_ChannelProcessor(tdms_channel=tdms_raw_CA[DATASET_NO ]['Wind Measurement']['Torque'])

# #%%
# wt.plot_filtered_th(100)
# #%%
# # gc_r = Graph_data_container(x=x_r,y = y_r, label = 'raw')
# # gc_f = Graph_data_container(x=x_f,y = y_f, label = df_tmp.iloc[:,1].name)


# plot_spect_comb2([wt.get_spectrum_raw(), wt.get_spectrum_filt(fc_Hz)], title='first attempt to show filter',
#                      xlim =[1e1,1e5],
#                 Kolmogorov_offset=1e2, to_disk=True)
# # # %%
# # plot_spect_comb2([gc_r], title='first attempt to show filter',
# #                      xlim =[1e1,1e5],
# #                 Kolmogorov_offset=1e2, to_disk=True)

# # # %%
# # plot_spect_comb2([gc_f], title=f'first attempt to show filter (cutoff: {fc_Hz}Hz)',
# #                      xlim =[1e1,1e5],
# #                 Kolmogorov_offset=5e0, to_disk=True)
# # %%
