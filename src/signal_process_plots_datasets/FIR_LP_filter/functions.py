#%%

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import pathlib

# FS=500_000  #Sampling frequency in Hz 

# Define a class to store the axis titles because they are repeating a lot
class Axis_titles:
    def __init__(self,x:str,y:str) -> None:
        self.x_title = x
        self.y_title = y
        

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

def spect (x:np.ndarray, FS:int):
    """
    # Welch's method for power spectrum
    
    Estimate the Power spectrum of a signal using the Welch method

    Args:
        x (np.ndarray):Column in dataframe managed as list of ndarrays.
        FS (int): The sampling frequency of the signal

    Returns:
       z(np.ndarray): Array of sample frequencies
       y(np.ndarray): Array of power spectrum of x
    """
    z,y = signal.welch(x,FS,window='flattop', nperseg=1_024, scaling='spectrum')
    return z, y
 
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

    
def plot_spect_comb2(graph_objlist ,
                    title:str, 
                    xlim = None, Kolmogorov_offset = None,
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
    for gdc_obj in graph_objlist:
        ax.scatter(gdc_obj.x, np.sqrt(gdc_obj.y), label=f'{gdc_obj.label}', s=1)
    
    try:
        plt.xlim(xlim)
    except:
        pass
    
    if Kolmogorov_offset is not None:
        KOLMOGORV_CONSTANT = - 5/3
        xs = np.array(graph_objlist[0].xs_lim)
        ys = xs**(KOLMOGORV_CONSTANT)*Kolmogorov_offset

        ax.plot(xs,ys, 'r--', label = 'Kolmogorov -5/3')
        ax.set_ylim(np.sqrt(graph_objlist[0].ys_lim))
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
#Define function to plot the raw and filtered signals combined 

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

class Signals_for_fft_plot:
    def __init__(self,freq,sig1:np.ndarray,sig2:np.ndarray) -> None:
        self.raw_mag = sig1
        self.filt_mag = sig2
        self.x = freq

class fft_calc_sig(Time_domain_data_cont):
    def __init__(self, x: np.ndarray, y: np.ndarray, label: str) -> None:
        super().__init__(x, y, label==None)
    
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

        yf_input = np.fft.fft(element.x)
        y_input_mag_plot = np.abs(yf_input)/fs
        f_plot = f[0:int(fs/2+1)]
        y_input_mag_plot = 2*y_input_mag_plot[0:int(fs/2+1)]
        y_input_mag_plot[0] = y_input_mag_plot[0] / 2

        yf_output = np.fft.fft(element.y)
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


# %%
