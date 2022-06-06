
from pathlib import Path
from matplotlib import pyplot as plt
import scipy.signal as signal
import numpy as np
import pandas as pd

import nptdms
from nptdms import TdmsFile

from functions import spect,  plot_spect_comb2, Graph_data_container
import logging
logging.basicConfig( level=logging.WARNING)


#%% Functions and classes
def filt_butter_factory( filt_order = 2):
    """this is a factory method that produces a BUTTERWORTH filter function 
    with a filter order and a cutoff frequency
    
    Args:
        filt_order (int, optional): Filter order. Defaults to 2.
        #TODO condider using also the fc_Hz as an argument so that the only parameters are:
        # the data and sampling frequnecy 
    """    
    def filt_butter(ds:np.ndarray, fs_Hz:float, fc_Hz:float, filt_order = filt_order ):
                    # filter cutoff frequency
        """applies filtering to np.array with fs_Hz data, with cuffoff frequency

        Args:
            ds (np.ndarray): _description_
            fs_Hz (float): _description_
            fc_Hz (int, optional): cutoff frequency of filter (low pass).Defaults to 100.
            filt_order (int, optional): _description_. Defaults to 2.

        Returns:
            _type_: _description_
        """                 
        sos = signal.butter(filt_order , fc_Hz, 'lp', fs=fs_Hz, output='sos')
        filtered = signal.sosfilt(sos, ds-ds[0])+ds[0]
        return filtered
    return filt_butter
filter_Butter_default=filt_butter_factory(filt_order = 5)

class WT_NoiseChannelProc():
    """
    Class for processing a tdms file for noise processing 
    """
    #TODO Consider using class methods to implement factory methods. (from tdms or ) 
    __measurement_history = []
    
    def __init__(self, desc:str, fs_Hz:float, data:np.ndarray, 
                 channel_name:str, group_name:str, _channel_data,
                 operations:list):
        self._channel_data= _channel_data
        self.set_description(desc=desc)
        # process details
        self.fs_Hz = fs_Hz
        self.data = data
        self.channel_name = channel_name
        self.group_name = group_name
        self.__measurement_history = operations
        
    def set_description(self, desc):
        """sets the description of the file

        Args:
            desc (_type_): _description_
        """        
        self.description = desc
    @property
    def operations(self):
        return self.__measurement_history
     
    @property
    def data_as_Series(self)->pd.Series:
        """returns the raw data as a pd.Series

        Returns:
            _type_: _description_
        """        
        return pd.Series(self.data, name=f'{self.channel_name}:raw')
    
    def get_averaged(self, fr_Hz:float=100, desc:str= None):
        """returns another object 

        Args:
            fr_Hz (float) : recording frequency (with averaging)
            desc (str) : description (Defaults to None: ie. add suffix _Av:<fr_Hz>)
        """        
        ds = self.data_as_Series
        fs_Hz = self.fs_Hz
            
        ds_fr = ds.groupby(ds.index// (fs_Hz/fr_Hz)).mean().values
        
        description = desc if desc is not None else self.description + f"_Av:{fr_Hz}"
        #TODO use factory method to return a new object. 
        new_operations = self.operations.copy()
        new_operations.append(f'Apply Averaging :{fr_Hz}')
        return WT_NoiseChannelProc(desc = description
                , fs_Hz=fr_Hz, data = ds_fr, 
                channel_name=self.channel_name, 
                group_name=self.group_name, _channel_data = None,
                operations = new_operations
                )
        
    def get_decimated(self, dec:int, offset:int=0):
        """returns a decimated data seires

        Args:
            dec (int): decimation factor
            offset (int): initial offset 

        Returns:
            _type_: a decimated data series. 
        """        
        decimated_fs_Hz = self.fs_Hz/dec
        
        new_operation = f'Decimation factor:{dec}, Offset:{offset}, new fs_Hz:{decimated_fs_Hz}'
        return WT_NoiseChannelProc.from_obj(self,
                operation=new_operation,  
                fs_Hz= decimated_fs_Hz, data=self.data[offset::dec])
    
    def filter(self, fc_Hz:float, filter_func=filter_Butter_default, fs_Hz=None )->pd.Series:
        """return a filtered signal based on 

        Args:
            fc_Hz (float): cut off frequency in Hz
            filter_func (filt_butter_factory, optional): filtering function that thates two arguments (ds, fs_Hz). Defaults to 100, filt_order = 2).
            fs_Hz (None): sampling frequency in Hz (#TODO SHOULD BE REMOVED)
            
        Returns:
            _type_: _description_
        """    
        if fs_Hz is not None:
            logging.warning(f'issued {fs_Hz} sampling frequency while the default is {self.fs_Hz}')
        fs_Hz = fs_Hz if fs_Hz is not None else self.fs_Hz
        filtered = filter_func(ds=self.data, fs_Hz=fs_Hz, fc_Hz=fc_Hz )
        return pd.Series(filtered, name=f'{self.channel_name}:filt_fc_{fc_Hz}')
    
    def filter_as_obj(self,  fc_Hz:float, filter_func=filter_Butter_default, fs_Hz=None, desc=None):
        ds_filt = self.filter( fc_Hz=fc_Hz, filter_func=filter_func, fs_Hz=fs_Hz )
        description = desc if desc is not None else self.description + f"_fc:{fc_Hz}"
        return WT_NoiseChannelProc.from_obj(self, 
            desc = description,
            data = ds_filt.values,
            operation = f'pass filter {fc_Hz}'
            )
    
    def get_spectrum_raw(self,window='flattop', nperseg=1_024, scaling='spectrum')->Graph_data_container:
        """returns a Graph_data_container object with the power spectrum of the data. 
        uses the decimation function

        Returns:
            _type_: _description_
        """        
        gobj = self.get_spectrum_raw_dec(dec=1, window=window,nperseg= nperseg, scaling=scaling)     
        return gobj
    
    
    def get_spectrum_raw_dec(self, dec:int=1, offset:int=0, window='flattop', nperseg=1_024, scaling='spectrum')->Graph_data_container:
        """returns a Graph_data_container object with the power spectrum of the **decimated** data. 

        Args:
            dec (int): decimation factor 
            offset (int, optional): offset. Defaults to 0.

        Returns:
            Graph_data_container: _description_
        """        
        decimated_fs_Hz = self.fs_Hz/dec
        x_r,y_r = spect(self.data[offset::dec], FS=decimated_fs_Hz,window=window,nperseg= nperseg, scaling=scaling)        
        if dec==1:
            label = f'{self.description}-{self.channel_name}'
        else:
            label = f'{self.description}-{self.channel_name}-fs:{decimated_fs_Hz/1000:.1f}kHz '
        return Graph_data_container(x=x_r,y = y_r, 
            label = label)
    
    
    def get_spectrum_filt(self, fc_Hz:float, filt_func=filter_Butter_default)->Graph_data_container:
        """returns a Graph_data_container object with the power spectrum of the data. 

        Args:
            fc_Hz (float): _description_

        Returns:
            Graph_data_container: _description_
        """        
        x_f,y_f = spect(self.filter(fc_Hz=fc_Hz, filter_func=filt_func), FS=self.fs_Hz)        
        return Graph_data_container(x=x_f,y = y_f, label = f'{self.description}-{self.channel_name} - filt: {fc_Hz}')
    
    def plot_filtered_th(self,fc_Hz):
        """plots the Time History

        Args:
            fc_Hz (_type_): _description_
        """        
        plt.plot(self.data, label = 'raw')
        plt.plot(self.filter(fc_Hz=fc_Hz), label = f'filtered: {fc_Hz}')


    
    @classmethod
    def from_tdms(cls, tdms_channel:nptdms.tdms.TdmsChannel, desc:str):
        """Factory methor that generates an object class
        #TOD need to change the init function and test. 

        Args:
            tdms_channel (nptdms.tdms.TdmsChannel): tmds channel 
            desc (str): descirption (used)
        """        
        _channel_data= tdms_channel
        # desc

        fs_Hz = 1/_channel_data.properties['wf_increment']
        data = _channel_data.data
        channel_name =_channel_data.name
        group_name = _channel_data.group_name
         
        return cls(desc, fs_Hz, data, channel_name, group_name, _channel_data, 
                   operations=[f'Loaded from tdms file {group_name}/{channel_name}, {fs_Hz}'])
    
    @classmethod
    def from_obj(cls, obj, operation:str=None, **kwargs):
        """Factory method that generates an object class
        if parameters are not provided the obj values are used. 
        
        Args:
            tdms_channel (nptdms.tdms.TdmsChannel): tmds channel 
            desc (str): descirption (used)
        """
        assert isinstance(operation, str)
        # the following line allows to pass a description maybe
        desc = obj.description if kwargs.get('desc', None) is None else kwargs.get('desc', None)
        
        _channel_data = kwargs.get('_channel_data', obj._channel_data)
        fs_Hz = kwargs.get('fs_Hz', obj.fs_Hz)
        data = kwargs.get('data', obj.data)
        channel_name = kwargs.get('channel_name', obj.channel_name)
        group_name = kwargs.get('group_name', obj.group_name)
        
        new_ops = obj.operations.copy()
        new_ops.append(operation)
        return cls(desc, fs_Hz, data, channel_name, group_name, _channel_data, 
            operations=new_ops)
# %%
