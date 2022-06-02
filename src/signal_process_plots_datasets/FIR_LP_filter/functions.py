#%%
from matplotlib import scale
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import pathlib
import pandas as pd
import nptdms
# FS=500_000  #Sampling frequency in Hz 

# Define function for Filter freq response

def plot_response(fs:float, w:np.ndarray, h:np.ndarray, title:str):
    """Plots the gain frequency response of the filter based on the coefficients
    Args:
        fs (float): sampling frequency. 
        w (np.ndarray): filter coefficients.
        h (np.ndarray): filter coefficients.
        title (str): title of plot. 
    """
    plt.figure()
    plt.plot(0.5*fs*w/np.pi, 20*np.log10(np.abs(h)))
    plt.ylim(-40, 5)
    #plt.xscale('log')
    #plt.xlim(0, 400)
    plt.grid(True)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Gain (dB)')
    plt.title(title)

#Define a function for Welch's method power spectrum for a signal

def spect (x:np.ndarray, FS:int, window='flattop', nperseg=1_024, scaling='spectrum'):
    """
    # Welch's method for power spectrum
    
    Estimate the Power spectrum of a signal using the Welch method
    Args:
        x (np.ndarray):Column in dataframe managed as list of ndarrays.
    Returns:
       z(np.ndarray): Array of sample frequencies
       y(np.ndarray): Array of power spectrum of x
    """
    z,y = signal.welch(x,FS,window=window, nperseg=nperseg, scaling=scaling)
    return z, y

#Define a function for plotting the Power spectrums

def plot_spectrum(x=np.ndarray,y=np.ndarray,
                title=str,xlim=None):
    """Plots the power spectrum from the results of spect() function
    Args:
        x (np.ndarray): frequencies calculated by Welch method (Hz).
        y (np.ndarray): the signal's power spectral magnitute from Welch method ().
        title (str): title of plot.
    """
    plt.figure()
    ax=plt.gca()
    ax.scatter(x, np.sqrt(y), s=5)
    ax.set_xscale('log')
    ax.set_yscale('log')
    plt.grid(True, which='both')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitute')
    plt.title(title)
    
    try:
        plt.xlim(xlim)
    except:
        pass

# Plot two spectrum diagrams of 2 different signals
# Should be replaced with plot_spect_comb2 function because 
# is more flexible than plot_spect_comb
#
# def plot_spect_comb(x1:np.ndarray,y1:np.ndarray,
#                     x2:np.ndarray,y2:np.ndarray,
#                     x3:np.ndarray, y3:np.ndarray,
#                     title:str, slabel1:str,slabel2:str,slabel3:str,
#                     xlim = None):
#     """ ## Three signals power spectrums combined in one graph
#     This function plots the power spectrum diagram of two signals.
#     The amplitute and frequency of the signals are calculated with signal.welch() function.
#     Args:
#         x1 (np.ndarray): The frequencies of the first given signal to be plotted
#         y1 (np.ndarray): The amplitute of the first given signal to be plotted
#         x2 (np.ndarray): The frequencies of the second given signal to be plotted
#         y2 (np.ndarray): The amplitute of the second given signal to be plotted
#         x3 (np.ndarray): The frequencies of the third given signal to be plotted
#         y3 (np.ndarray): The amplitute of the third given signal to be plotted
#         title (str): The main title of the figure 
#         slabel1 (str): The label to be presented in the legend of the plot for the first signal
#         slabel2 (str): The label to be presented in the legend of the plot for the second signal
#         slabel2 (str): The label to be presented in the legend of the plot for the third signal
#     """
#     plt.figure()
#     ax = plt.gca()
#     ax.scatter(x1, np.sqrt(y1), label=f'{slabel1}', s=1)
#     ax.scatter(x2, np.sqrt(y2), label=f'{slabel2}', s=1)
#     ax.scatter(x3, np.sqrt(y3), label=f'{slabel3}', s=1)
# 
#     ax.set_xscale('log')
#     ax.set_yscale('log')
#     plt.grid(True, which='both')
#     plt.xlabel('Frequency [Hz]')
#     plt.ylabel('Amplitute')
#     plt.legend(bbox_to_anchor=(1.04,0.5))
#     plt.title(title)
#     
#     try:
#         plt.xlim(xlim)
#     except:
#         pass
 
 
class Graph_data_container:
    def __init__(self, x:np.ndarray, y:np.ndarray, label:str) -> None:
        self.x = x
        self.y = y
        self.label = label
    
    @property 
    def xs_lim(self):
        x_l =  np.floor(np.log10 (max(1, min(self.x)) ))
        x_u =  np.ceil(np.log10 (max(1, max(self.x)) ))
        return [10**x_l, 10**x_u]
    @property 
    def ys_lim(self):
        x_l =  np.floor(np.log10 ( min(self.y) ))-1
        x_u =  np.ceil(np.log10 ( max(self.y) ))+1
        return [10**x_l, 10**x_u]
    
    @property 
    def extrema(self):
        """returns the extreme values for x and y 
        [x_min, x_max, y_min, y_max]
        Returns:
            _type_: _description_
        """        
        return [self.x.min(), self.x.max(), self.y.min(), self.y.max()]

    
def plot_spect_comb2(graph_objlist ,
                    title:str, 
                    xlim = None, 
                    ylim = 'auto',
                    Kolmogorov_offset = None,
                    **kwargs,
                    ):
    """ ## plots different signal power spectrums combined in one graph
    This function plots the power spectrum diagram of an arbitray  signals.
    The amplitute and frequency of the signals are calculated with signal.welch() function.
    Args:
        graph_objlist(list): a list of Graph_data_container
        title (str): The main title of the figure 
        xlim (tuple): x limits of power spectrum graph
    """
    fig, ax = plt.subplots(1,1, figsize=kwargs.get('figsize',None))
    xylims = []
    for gdc_obj in graph_objlist:
        assert isinstance(gdc_obj, Graph_data_container)
        ax.scatter(gdc_obj.x, np.sqrt(gdc_obj.y), label=f'{gdc_obj.label}', s=kwargs.get('markersize',2))
        xylims.append(gdc_obj.extrema)
    
    
    try:
        plt.xlim(xlim)
    except:
        pass
    
    if Kolmogorov_offset is not None:
        KOLMOGORV_CONSTANT = - 5/3
        xs = np.array(graph_objlist[0].xs_lim)
        ys = xs**(KOLMOGORV_CONSTANT)*Kolmogorov_offset

        ax.plot(xs,ys, 'r--', label = 'Kolmogorov -5/3')
    if ylim == 'auto':
        arr= np.array(xylims)[:,2:]
        ax.set_ylim(np.sqrt([arr[:,0].min(), arr[:,1].max() ]))
        
    elif isinstance(ylim, list):
        ax.set_ylim( ylim)
    # final formating
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.grid(True, which='both')
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Amplitute')
    # plt.legend(bbox_to_anchor=(1.04,0.5))
    ax.legend()
    ax.set_title(title)
    if kwargs.get('to_disk', None) is True:
        target_path = pathlib.Path('_temp_fig/{}.png'.format(title.translate({ord(c): None for c in ': /='} )))
        target_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(target_path,facecolor='white', transparent=False)
    
#%%    
# New classes for storing signal and titles information for human readable code 
# and faster implementation regardless the actual operation of a function
class Axis_titles:
    def __init__(self, x:str, y:str) -> None:
        self.x_title = x
        self.y_title = y

class Time_domain_data_cont():
    """A class for importing the x,y variables for a signal in time domain
    to plotting functions.
    """

    def __init__(self,x:np.ndarray,y:np.ndarray,label:str) -> None:
        """_summary_

        Args:
            x (np.ndarray): time duration of the signal in seconds.
            y (np.ndarray): amplitute in dB (decibel)
            label (str): signal information for the figure legend
        """
        self.x = x
        self.y = y
        self.label = label
     

#Define function to plot the raw and filtered signals combined 
# This function could be replaced with the new one
#
# def plot_signals(x_1:np.ndarray,x_2:np.ndarray,
#                 y_1:np.ndarray,y_2:np.ndarray,
#                 Title:str):
#     """Plot the filtered signal in combined plots for comparison with the raw signal
#     Args:
#         x_1 (np.ndarray): time interval of raw signal.
#         x_2 (np.ndarray): time interval of filtered signal.
#         y_1 (np.ndarray): ndArray for each dataframe column (from raw signal).
#         y_2 (list): same as y_1 for filtered signal. 
#         Title (str): a list with titles discribing the system condition (connected inverter or not etc.).
#     """
#     plt.title(Title)
#     plt.scatter(x_1, y_1, label= 'Raw signal', alpha=0.2)
#     plt.plot(x_2, y_2, label='Filtered signal', color= 'r')
#     plt.grid(True)
#     plt.xlabel('Time [s]')
#     plt.ylabel('Amplitute')
#     plt.legend(loc='lower right')
#     plt.show()
def plot_signals(time_domain_sig,
                axis_titles:str,
                Title:str,
                **kwargs,
                ):
    """ ## Plot signals in time domain
    This function is used to plot signals in time domain from the old dataset.
    It was updated to use class objects as import for the x,y components of the signal and
    the axis titles instead of a variable oriented import (old plot_signals function)
    which was more static and ram consuming.


    Args:
        time_domain_sig (list): A list created from Time_domain_data_cont
        axis_titles (str): The axis titles
        Title (str): The titles to be plotted in each figure

    """
    fig, ax = plt.subplots(1,1, figsize=kwargs.get('figsize',None))
    for obj in time_domain_sig:
        ax.scatter(obj.x,obj.y, label=f'{obj.label}', s=1)

    for ax_title in axis_titles:
        ax.set_title(Title)
        ax.set_ylabel(ax_title.y_title)
        ax.set_xlabel(ax_title.x_title)
        ax.grid(True, which='both')
        ax.legend(bbox_to_anchor=(1.04,0.5))

#Define function for ploting the signals in seperate graphs
# 
# This function is not needed. The original use was for my better understanding
# in early process of .h5 dataframe.
#  
# def plot_sep_sig(x_1:np.ndarray, y_1:np.ndarray, x_2:np.ndarray, y_2:np.ndarray, TITLE:str, TITLE_2:str, color:str):
#     """
#     Plots of the filtered and raw signal in separate figures 
#     for better understanding of the system response to the filter 
#     Args:
#         x_1 (np.ndarray): time interval of measurment.
#         y_1 (np.ndarray): raw signal from sensor. 
#         x_2 (np.ndarray): time interval of filtered samples.
#         y_2 (np.ndarray):  filtered signal after process.
#         TITLE (str): Title for figure with raw data.
#         TITLE_2 (str): Title for figure with filtered data. 
#         color (str): the color for each plot of filtered signal(connected(off=red, on=yellow, on_and_wind_speed=black), same for disconnected). 
#     """
#     plt.title(TITLE)
#     plt.grid(True)
#     plt.xlabel('Time [s]')
#     plt.ylabel('Amplitute')
#     plt.plot(x_1, y_1)
#     plt.show()
# 
#     plt.title(TITLE_2)
#     plt.grid(True)
#     plt.xlabel('Time [s]')
#     plt.ylabel('Amplitute')
#     plt.plot(x_2, y_2, color, linewidth= 1)
#     plt.show()

#Define function for FFT of two signals to be able of plotting 
#the corrupted and uncorrupted signals in frequency domain
# 
# This function will be replaced to use as input a class object. This is because 
# will be much easier to use it in the application. (I think....?!?!?)
#  
# def fft_sig (y1:np.ndarray, y2:np.ndarray,    f0 = 2_000,fs = 500_000):
#     """
#     Computes the fourier transform for two seperate signals and returns the results
#     and the corresponding frequencies
#     Args:
#         y1 (np.ndarray): array object corresponding to raw signal.
#         y2 (np.ndarray): array object corresponding to filtered signal.
#     
#     Returns:
#        f_plot(np.ndarray): array_like of sample frequencies
#        y_input_mag_plot(np.ndarray): Amplitude of raw signal samples
#        y_output_mag_plot(np.ndarray): Amplitude of filtered signal samples
#     """
# 
#     N = int(2_000*(fs/f0)) #TODO what is this N???
#     f= np.linspace (0, (N-1)*(fs/N),N )
# 
#     yf_input = np.fft.fft(y1)
#     y_input_mag_plot = np.abs(yf_input)/N
#     f_plot = f[0:int(N/2+1)]
#     y_input_mag_plot = 2*y_input_mag_plot[0:int(N/2+1)]
#     y_input_mag_plot[0] = y_input_mag_plot[0] / 2
# 
#     yf_output = np.fft.fft(y2)
#     y_output_mag_plot = np.abs(yf_output)/N
#     y_output_mag_plot = 2* y_output_mag_plot[0:int(N/2+1)]
#     y_output_mag_plot[0]= y_output_mag_plot[0]/2
#     return(f_plot, y_input_mag_plot, y_output_mag_plot)

class Signals_for_fft_plot:
    def __init__(self,freq,sig1:np.ndarray,sig2:np.ndarray) -> None:
        self.raw_mag = sig1
        self.filt_mag = sig2
        self.x = freq

class fft_calc_sig:
    def __init__(self, x1: np.ndarray, x2: np.ndarray, label: str) -> None:
        self.x1 = x1
        self.x2 = x2

#Define function for FFT of two signals to be able of plotting
#the corrupted and uncorrupted signals in frequency domain
def fft_sig (signals,    f0 = 2_000,fs = 500_000):
    """
    Computes the fourier transform for two seperate signals and returns the results
    and the corresponding frequencies

    Args:
        y1 (np.ndarray): array object corresponding to raw signal.
        y2 (np.ndarray): array object corresponding to filtered signal.

    Returns:
       f_plot(np.ndarray): array_like of sample frequencies
       y_input_mag_plot(np.ndarray): Amplitude of raw signal samples
       y_output_mag_plot(np.ndarray): Amplitude of filtered signal samples

    """

    N = int(2_000*(fs/f0)) #TODO what is this N???
    # This N was used in a video which i found on Youtube for computing and
    # plotting the FFT of a signal.
    # Even the guy in the video was not sure why to use this N but
    # fs is the sampling frequency and f0 is the signal frequency.
    # I multiply with 2_000 to eliminate the signal frequency and use it as
    # the sampling frequency for plotting the signal in freq domain (x axis).
    # #TODO have to find something better couse it's a black box for me
    # and the source is unreliable

    f= np.linspace (0, (fs-1), fs)
    for element in signals:

        yf_input = np.fft.fft(element.x1)
        y_input_mag_plot = np.abs(yf_input)/fs
        f_plot = f[0:int(fs/2+1)]
        y_input_mag_plot = 2*y_input_mag_plot[0:int(fs/2+1)]
        y_input_mag_plot[0] = y_input_mag_plot[0] / 2

        yf_output = np.fft.fft(element.x2)
        y_output_mag_plot = np.abs(yf_output)/fs
        y_output_mag_plot = 2* y_output_mag_plot[0:int(fs/2+1)]
        y_output_mag_plot[0]= y_output_mag_plot[0]/2


    # dt = 0.01              # time interval
    # t=np.arange(0,7.5,dt)     # time array
    # n=len(t)                # number of samples
    # fhat = np.fft.fft(y1,n) # compute the fft for the first signal
    # PSD = fhat * np.conj(fhat) / n
    # freq = (1/(dt*n)) * np.arange(n)
    # L = np.arange(1,np.floor(n/2), dtype='int')


    return(f_plot, y_input_mag_plot, y_output_mag_plot,
            #freq, L, PSD
            )


#Define function for the FFT plot
# This function will be written to use class objects for more ease of use in 
# importing and not to be bound to variables for less RAM usage
#  
# def plot_FFT (x1=np.ndarray, y1=np.ndarray, y2=np.ndarray, title=list):
#     """
#     Function for plotting the raw and filtered signals in
#     frequency domain. On the x axis we plot the frequency in Hz 
#     and on the y axis the amlitude of the sample at that frequency
#     Args:
#         x1 (np.ndarray): frequencies of samples(f_plot).
#         y1 (np.ndarray): Amplitude in [dB] of raw signal samples in freq. domain. 
#         y2 (np.ndarray): Amplitude in [dB] of filtered signal samples in freq. domain.
#         title (list): List of titles for all the plots.
#     """    
#     fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, sharey=True)
#     fig.suptitle(title)
#     ax1.loglog(x1, y1)
#     ax1.grid(True, which = 'both')
#     ax1.set_ylabel('Amplitute [dB]')
#     ax2.loglog(x1, y2, 'orange', label = 'output')
#     ax2.grid(True, which='both')
#     ax2.set_xlabel('Frequency [Hz]')
#     ax2.set_ylabel('Amplitute [dB]')
#     plt.legend()
#     plt.show()
class Fft_Plot_info:
    def __init__(self, Title:list, filter_type:str, signal_state:str) -> None:
        """Initiate a class for importing information used in fft graph

        Args:
            Title (list): The titles to be presented in each graph
            explaining the device's configuration for each measurement.

    ### Filtering process information:
    #### Figure label information for plotting in output graph

        filter_type (str): The filter type used to produce the output

        signal_state (str): This defines if there is a corruption during the
        filtering process
        """
        self.title = Title
        self.filt_type = filter_type
        self.sig_state = signal_state

#Define function for the FFT plot
def plot_FFT (signals,
                info,
                axis_titles:str,
                **kwargs
                ):
    """
    Function for plotting the raw and filtered signals in
    frequency domain. On the x axis we plot the frequency in Hz
    and on the y axis the amplitude of the sample at that frequency

    Args:
        signals (_type_): Class object with the raw signal
        info (_type_): Information for the legend
        axis_titles (str): X,Y axis titles
    """

    for objct,obj,ax_titles in zip(signals, info, axis_titles):
        fig, (ax1, ax2) = plt.subplots(2, 1,
                                        sharex=True, sharey=True,
                                        figsize=kwargs.get('figsize',None))

        fig.suptitle(obj.title)
        ax1.loglog(objct.x, objct.raw_mag)
        ax1.grid(True, which = 'both')
        ax1.set_ylabel(ax_titles.y_title)
        ax2.loglog(objct.x, objct.filt_mag, 'orange',
                    label = f'{obj.sig_state} {obj.filt_type} output')

        ax2.grid(True, which='both')
        ax2.set_xlabel(ax_titles.x_title)
        ax2.set_ylabel(ax_titles.y_title)
        plt.legend()
        plt.show()

# Adding WT_Noise_ChannelProcessor to use the signal info from nptdms 
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

def data_import(file_path:str, file_name_of_raw:str):
    """file import script and data chunking for faster overall process time

    Args:
        file_path (str): the file path of the folder containing the HDF5 file
        file_name_of_raw (str): the name of the file to import
    Returns:
        MATRIX_RAW (list): a list of np.ndarrays transformed columns from dataset
        L (list): a list of the dataframes keys in str format
        List_of_chunked (list): Here we store the sampled raw
        signal from the dataset with a constant rate 

    """

    # #Read and store the .h5 file with pandas
    # f_1 = pd.HDFStore(path='/home/goodvibrations32/Documents/Git_clones_dissertation/DSP_Filters_Python-/src/data_folder/noise_reference_raw.h5', mode='r')
    # 
    # #Store all the dataframe in a variable
    # data_raw = f_1['/df']
    # 

    #file_path = input('The full path of raw data file to process: ' )
    #file_name_of_raw =input('Enter the name of the raw signal file :') 

    #Read and store the .h5 file with pandas
    f_1 = pd.HDFStore(path=f'{file_path}{file_name_of_raw}', mode='r')

    print('The data frame key is: ',f_1.keys())


    data_raw = f_1['df']

    #Chunking of data with a constant sample rate
    rate_of_sampling = 10

    chunked_data = data_raw[::rate_of_sampling]
    List_of_chunked = []

    #Make a list with present keys
    L = list(data_raw.keys())

    #Store the chunked data in a list for the signal processing operations
    for element1 in L:
        List_of_chunked.append(np.array(chunked_data.get(element1)))
    print(data_raw.info())

    #Manage data with lists 
    MATRIX_RAW = []
    for element0 in L:
        MATRIX_RAW.append(np.array(data_raw.get(element0)))
    
    return MATRIX_RAW, L, List_of_chunked