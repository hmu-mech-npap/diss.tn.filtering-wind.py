
# %%
#Use of pandas library for reading hdf5 file format

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal

#%%
# Define function for Filter freq response

def plot_response(fs, w, h, title):
    plt.figure()
    plt.plot(0.5*fs*w/np.pi, 20*np.log10(np.abs(h)))
    plt.ylim(-40, 5)
    #plt.xscale('log')
    plt.xlim(0, 400)
    plt.grid(True)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Gain (dB)')
    plt.title(title)

#%%
#Define a function for Welch's method power spectrum for a signal

def spect (x):
    x,y = signal.welch(x,FS,window='flattop', nperseg=1024, scaling='spectrum')
    return x, y

#%%
#Define a function for plotting the Power spectrums

def plot_spectrum(x, y, title):
    plt.figure()
    plt.semilogy(x, np.sqrt(y))
    plt.grid(True, which='both')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Linear spectrum [V RMS]')
    plt.title(title)


#%%
#Define function to plot the raw and filtered signals combined 

def plot_signals(x1,x2,y1,y2,Title):
    plt.title(Title)
    plt.plot(x1, y1, label= 'Raw signal')
    plt.plot(x2, y2, label='Filtered signal')
    plt.grid(True)
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitute')
    plt.legend(loc='lower right')
    plt.show()


#%%
#Define function for ploting the signals in seperate graphs
def plot_sep_sig(x_1, y_1, x_2, y_2, TITLE, TITLE_2, color):
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

#%%
#Define function for FFT of two signals to be able of plotting 
#the corrupted and uncorrupted signals in frequency domain
def fft_sig (y1, y2):
    f0 = 2000
    fs = 500000
    N = int(2000*(fs/f0))
    yf_input = np.fft.fft(y1)
    y_input_mag_plot = np.abs(yf_input)/N
    f= np.linspace (0, (N-1)*(fs/N),N )
    f_plot = f[0:int(N/2+1)]
    y_input_mag_plot = 2*y_input_mag_plot[0:int(N/2+1)]
    y_input_mag_plot[0] = y_input_mag_plot[0] / 2

    yf_output = np.fft.fft(y2)
    y_output_mag_plot = np.abs(yf_output)/N
    y_output_mag_plot = 2* y_output_mag_plot[0:int(N/2+1)]
    y_output_mag_plot[0]= y_output_mag_plot[0]/2
    return(f_plot, y_input_mag_plot, y_output_mag_plot)

#%%
#Define function for the FFT plot
def plot_FFT (x1, y1, y2, title):
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, sharey=True)
    fig.suptitle(title)
    ax1.semilogx(x1, y1)
    ax1.grid(True, which = 'both')
    ax1.set_ylabel('Amplitute [dB]')
    ax2.semilogx(x1, y2, 'orange', label = 'output')
    ax2.grid(True, which='both')
    ax2.set_xlabel('Frequency [Hz]')
    ax2.set_ylabel('Amplitute [dB]')
    plt.ylim(0, 0.020)
    plt.legend()
    plt.show()

#%%
#Read and store the .h5 file with pandas
f_1 = pd.HDFStore(path='/run/media/goodvibrations32/KINGSTON/_noiseReference_2021/20210831/noise_reference_raw.h5', mode='r')

data_raw = f_1['/df']


#%%
#Make a list for the keys present in the data frame
L = list(data_raw.keys())

#Manage data with lists 
MATRIX_RAW = []
for element0 in L:
    MATRIX_RAW.append(np.array(data_raw.get(element0)))


#%%
#The only filter with les standard deviation on output from input
#Somehow should test more of these kind of filters with no window functions 

#FIR Low-pass filter on the signal with the inverter connected and off

#The length of the filter(number of coefficients, the filter order + 1)
numtaps_2 = 2_000
FS = 500_000
cutoff_hz = 0.00001

#Use of firwin to create low-pass FIR filter
fir_co = signal.firwin(numtaps_2, cutoff_hz)
w_fir_co, h_fir_co = signal.freqz(fir_co, [1])

#%%
#Plot the freq response of the filter
plot_response(FS, w_fir_co, h_fir_co, 'Blank FIR filter')

#%%
#Filtering the raw signal with the above FIR filter 
MATRIX_FILT = [] 
x=[]
for item in MATRIX_RAW:
    x=signal.lfilter(fir_co, 1.0, item)
    MATRIX_FILT.append(x)


#%%

#Time interval of the samples
TIME = np.linspace(0, 7.599998, 3_800_000)

#The first N-1 samples are corrupted by the initial conditions
warmup = numtaps_2 - 1

#The phase delay of the filtered signal
delay= (warmup / 2) / FS

TIME_NO_SHIFT = TIME[warmup:]-delay

#%%
#Uncorrupted signal
UNCORR = []
for item in MATRIX_FILT:
    UNCORR.append(item[warmup:])

#%%

#Plot of the raw and filtered signals in one graph with different colors for 
#better understanding the response of the filter at the system in time domain

Titles = ['Inverter connected and off','Inverter connected and on','Inverter connected, on and wind speed 5 [m/s]','Inverter disconnected and off','Inverter disconnected and on','Inverter disconnected, on and Wind speed 5 [m/s]']
# for simultaneously looping through lists
for i,j,k in zip(MATRIX_RAW, UNCORR, Titles):

    plot_signals(TIME,TIME_NO_SHIFT,i,j,k)

#%%
#List the titles and colores that are to be plotted
raw_titles = ['Raw signal Inverter connected and off','Raw signal Inverter connected and on','Raw signal Inverter connected, on and wind speed 5 [m/s]','Raw signal with Inverter disconnected and off','Raw signal with Inverter disconnected and on','Raw signal with Inverter disconnected, on and Wind speed 5 [m/s]']
filt_titles = ['Filtered signal Inverter connected and off','Filtered signal Inverter connected and on','Filtered signal Inverter connected, on and wind speed 5 [m/s]','Filtered signal with Inverter disconnected and off','Filtered signal with Inverter disconnected and on','Filtered signal with Inverter disconnected, on and Wind speed 5 [m/s]']
colors_filt = ['r','y','black','r','y','black']

#Plot the original and filtered signal (uncorrupted) in different plots for graphical comparison
# of the two methods of filtering (lazy approach branch and High res). 
for i,j,t,f,c in zip(MATRIX_RAW, UNCORR, raw_titles, filt_titles, colors_filt):
    plot_sep_sig(TIME, i, TIME_NO_SHIFT, j, t, f, c)

# %%
#List the titles to be plotted in Power spectrum
raw_titles_spec = ['Raw signal Power spectrum (Inverter connected and off)','Raw signal Power spectrum (Inverter connected and on)','Raw signal Power spectrum (Inverter connected, on and WS=5m/s)','Raw signal Power spectrum (Inverter disconnected and off)','Raw signal Power spectrum (Inverter disconnected and on)','Raw signal Power Spectrum (Inverter disconnected, on and WS=5m/s)']
filt_titles_spec = ['Filtered signal Power spectrum (Inverter connected and off)','Filtered signal Power spectrum (Inverter connected and on)','Filtered signal Power Spectrum (Inverter connected, on and WS=5m/s)','Filtered signal Power Spectrum (Inverter disconnected and off)','Filtered signal Power Spectrum (Inverter disconnected and on)','Filtered signal Power Spectrum (Inverter disconnected, on and WS=5m/s)']

#Plot the raw and filtered signals spectrums with titles 
for i,j,t3,t4 in zip(MATRIX_RAW, UNCORR, raw_titles_spec, filt_titles_spec):
    f_r, Prr_spec = spect(i)
    plot_spectrum(f_r, Prr_spec,t3)
    f_f, Pff_spec = spect(j)
    plot_spectrum(f_f, Pff_spec, t4)


#%%
#List the titles for the Frequency domain plots of the corrupted and uncorrupted samples
blank_freq_dom_titles = ['Blank filter output with Inverter connected, off','Blank filter output with Inverter connected, on','Blank filter output with Inverter connected, on and WS=5[m/s]','Blank filter output with Inverter disconnected, off','Blank filter output with Inverter disconnected, on','Blank filter output with Inverter disconnected, on and WS=5[m/s]']
shifted_freq_dom_titles = ['Not shifted filter output with Inverter connected, off','Not shifted filter output with Inverter connected, on', 'Not shifted filter output with Inverter connected, on and WS=5[m/s]','Not shifted filter output with Inverter disconnected, off','Not shifted filter output with Inverter disconnected, on','Not shifted filter output with Inverter disconnected, on and WS=5[m/s]']

#Compute the FFT of raw, corrupted and uncorrupted signals and plot them combined for comparison 
for i,j,k,t1,t2 in zip(MATRIX_RAW,MATRIX_FILT,UNCORR,blank_freq_dom_titles,shifted_freq_dom_titles):
    f,yin,yout= fft_sig(i,j)
    plot_FFT(f,yin,yout,t1)
    
    f_sh,yin_sh,yout_sh =fft_sig(i,k)
    plot_FFT(f_sh,yin_sh,yout_sh,t2)


# %%
