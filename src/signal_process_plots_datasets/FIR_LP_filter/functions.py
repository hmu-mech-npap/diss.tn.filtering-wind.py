#%%
from matplotlib import scale
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

FS=500_000  #Sampling frequency in Hz 

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

def spect (x:np.ndarray):
    """
    # Welch's method for power spectrum
    
    Estimate the Power spectrum of a signal using the Welch method

    Args:
        x (np.ndarray):Column in dataframe managed as list of ndarrays.

    Returns:
       z(np.ndarray): Array of sample frequencies
       y(np.ndarray): Array of power spectrum of x
    """
    z,y = signal.welch(x,FS,window='flattop', nperseg=1_024, scaling='spectrum')
    return z, y

#Define a function for plotting the Power spectrums

def plot_spectrum(x=np.ndarray, y=np.ndarray, title=str):
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

# Plot two spectrum diagrams of 2 different signals

def plot_spect_comb(x1:np.ndarray,y1:np.ndarray,x2:np.ndarray,y2:np.ndarray,x3:np.ndarray, y3:np.ndarray,title:str, slabel1:str,slabel2:str,slabel3:str):
    """ ## Three signals power spectrums combined in one graph

    This function plots the power spectrum diagram of two signals.
    The amplitute and frequency of the signals are calculated with signal.welch() function.

    Args:
        x1 (np.ndarray): The frequencies of the first given signal to be plotted
        y1 (np.ndarray): The amplitute of the first given signal to be plotted
        x2 (np.ndarray): The frequencies of the second given signal to be plotted
        y2 (np.ndarray): The amplitute of the second given signal to be plotted
        x3 (np.ndarray): The frequencies of the third given signal to be plotted
        y3 (np.ndarray): The amplitute of the third given signal to be plotted
        title (str): The main title of the figure 
        slabel1 (str): The label to be presented in the legend of the plot for the first signal
        slabel2 (str): The label to be presented in the legend of the plot for the second signal
        slabel2 (str): The label to be presented in the legend of the plot for the third signal
    """
    plt.figure()
    ax = plt.gca()
    ax.scatter(x1, np.sqrt(y1), label=f'{slabel1}', s=1)
    ax.scatter(x2, np.sqrt(y2), label=f'{slabel2}', s=1)
    ax.scatter(x3, np.sqrt(y3), label=f'{slabel3}', s=1)

    ax.set_xscale('log')
    ax.set_yscale('log')
    plt.grid(True, which='both')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitute')
    plt.legend(bbox_to_anchor=(1.04,0.5))
    plt.title(title)

#Define function to plot the raw and filtered signals combined 

def plot_signals(x_1:np.ndarray, x_2:np.ndarray, y_1:np.ndarray, y_2:np.ndarray, Title:str):
    """Plot the filtered signal in combined plots for comparison with the raw signal

    Args:
        x_1 (np.ndarray): time interval of raw signal.
        x_2 (np.ndarray): time interval of filtered signal.
        y_1 (np.ndarray): ndArray for each dataframe column (from raw signal).
        y_2 (list): same as y_1 for filtered signal. 
        Title (str): a list with titles discribing the system condition (connected inverter or not etc.).
    """
    plt.title(Title)
    plt.scatter(x_1, y_1, label= 'Raw signal', alpha=0.2)
    plt.plot(x_2, y_2, label='Filtered signal', color= 'r')
    plt.grid(True)
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitute')
    plt.legend(loc='lower right')
    plt.show()


#Define function for ploting the signals in seperate graphs
def plot_sep_sig(x_1:np.ndarray, y_1:np.ndarray, x_2:np.ndarray, y_2:np.ndarray, TITLE:str, TITLE_2:str, color:str):
    """
    Plots of the filtered and raw signal in separate figures 
    for better understanding of the system response to the filter 

    Args:
        x_1 (np.ndarray): time interval of measurment.
        y_1 (np.ndarray): raw signal from sensor. 
        x_2 (np.ndarray): time interval of filtered samples.
        y_2 (np.ndarray):  filtered signal after process.
        TITLE (str): Title for figure with raw data.
        TITLE_2 (str): Title for figure with filtered data. 
        color (str): the color for each plot of filtered signal(connected(off=red, on=yellow, on_and_wind_speed=black), same for disconnected). 
    """
    plt.title(TITLE)
    plt.grid(True)
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitute')
    plt.plot(x_1, y_1)
    plt.show()

    plt.title(TITLE_2)
    plt.grid(True)
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitute')
    plt.plot(x_2, y_2, color, linewidth= 1)
    plt.show()

#Define function for FFT of two signals to be able of plotting 
#the corrupted and uncorrupted signals in frequency domain
def fft_sig (y1:np.ndarray, y2:np.ndarray):
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
    f0 = 2_000
    fs = 500_000
    N = int(2_000*(fs/f0))
    f= np.linspace (0, (N-1)*(fs/N),N )

    yf_input = np.fft.fft(y1)
    y_input_mag_plot = np.abs(yf_input)/N
    f_plot = f[0:int(N/2+1)]
    y_input_mag_plot = 2*y_input_mag_plot[0:int(N/2+1)]
    y_input_mag_plot[0] = y_input_mag_plot[0] / 2

    yf_output = np.fft.fft(y2)
    y_output_mag_plot = np.abs(yf_output)/N
    y_output_mag_plot = 2* y_output_mag_plot[0:int(N/2+1)]
    y_output_mag_plot[0]= y_output_mag_plot[0]/2
    return(f_plot, y_input_mag_plot, y_output_mag_plot)

#Define function for the FFT plot
def plot_FFT (x1=np.ndarray, y1=np.ndarray, y2=np.ndarray, title=list):
    """
    Function for plotting the raw and filtered signals in
    frequency domain. On the x axis we plot the frequency in Hz 
    and on the y axis the amlitude of the sample at that frequency

    Args:
        x1 (np.ndarray): frequencies of samples(f_plot).
        y1 (np.ndarray): Amplitude in [dB] of raw signal samples in freq. domain. 
        y2 (np.ndarray): Amplitude in [dB] of filtered signal samples in freq. domain.
        title (list): List of titles for all the plots.
    """    
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, sharey=True)
    fig.suptitle(title)
    ax1.loglog(x1, y1)
    ax1.grid(True, which = 'both')
    ax1.set_ylabel('Amplitute [dB]')
    ax2.loglog(x1, y2, 'orange', label = 'output')
    ax2.grid(True, which='both')
    ax2.set_xlabel('Frequency [Hz]')
    ax2.set_ylabel('Amplitute [dB]')
    plt.legend()
    plt.show()

# %%
