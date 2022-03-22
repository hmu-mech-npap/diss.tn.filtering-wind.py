
# %%
#Use of pandas library for reading hdf5 file format

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
from pylab import plot, grid, show, ylim, title

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
#Define function for FFT
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
f_1 = pd.HDFStore(path='/run/media/goodvibrations/KINGSTON/_noiseReference_2021/20210831/noise_reference_raw.h5', mode='r')

data_raw = f_1['/df']

#%%
#Store the measurment in one dimentional array and transform it in numpy ndarray for processing 

first_column =data_raw.get('raw-2021.08.31-12:26:54')
sig_inverter_con_off = np.array(first_column)

first_column.info()

#%%
second_column = data_raw.get('raw-2021.08.31-12:28:24')
sig_inverter_con_on = np.array(second_column)

#%%
third_column = data_raw.get('raw-2021.08.31-12:32:08')
sig_inverter_con_on_WS_5 = np.array(third_column)

#%%
fourth_column = data_raw.get('raw-2021.08.31-12:34:29')
sig_inverter_discon_off = np.array(fourth_column)

#%%
fifth_column = data_raw.get('raw-2021.08.31-12:35:42')
sig_inverter_discon_on = np.array(fifth_column)

#%%
sixth_column = data_raw.get('raw-2021.08.31-12:37:45')
sig_inverter_discon_on_WS_5 = np.array(sixth_column)

#%%
print (first_column.head())

#%%
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


#%%
#Plot the freq response of the filter
plot_response(fs, w_fir_co, h_fir_co, 'Blank FIR filter')


#%%
#Apply the filter to the signal column by column from the data set

blank_lp_fir_con_off = signal.lfilter(fir_co, 1.0, sig_inverter_con_off)

#%%
blank_lp_fir_con_on = signal.lfilter(fir_co, 1.0, sig_inverter_con_on)

#%%
blank_lp_fir_con_on_WS_5 = signal.lfilter(fir_co, 1.0, sig_inverter_con_on_WS_5)

#%%
blank_lp_fir_discon_off = signal.lfilter(fir_co, 1.0, sig_inverter_discon_off)

#%%
blank_lp_fir_discon_on = signal.lfilter(fir_co, 1.0, sig_inverter_discon_on)

#%%
blank_lp_fir_discon_on_WS_5 = signal.lfilter(fir_co, 1.0, sig_inverter_discon_on_WS_5)


#%%
#This raises an error for incompatible shapes of the arrays 
#but all H1, H2, H3, H4 have same shape (3800000,)

# Transfer function of the FIR filter (z-Transform)
# H(z) = Y(z) / X(z)
time = np.linspace(0, 7.599998, 3800000)

H1 = blank_lp_fir_con_off/ sig_inverter_con_off

sys = signal.TransferFunction(w_fir_co, h_fir_co)
 
H2 = blank_lp_fir_con_on/ sig_inverter_con_on
H3 = blank_lp_fir_con_on_WS_5/ sig_inverter_con_on_WS_5
H4 = blank_lp_fir_discon_off/ sig_inverter_discon_off

# sys= signal.lti(H1, H2, H3, H4)

w, mag, phase = signal.bode(sys)
plt.show()
#%%
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
#This plot is for the blank signal with shift and amplitute gain

title('Filtered signal with phase shift with Inverter connected and off')

plot(time-delay, blank_lp_fir_con_off, 'g-')

grid(True)

ylim((1.585,1.595))

show()


#%%
#Plot of the raw and filtered signals in one graph with different colors for 
#better understanding the response of the system in time domain

#===============================================
#Inverter connected and off
#===============================================
#figure(1)

plot_signals(time,time_no_shift,sig_inverter_con_off,filt_con_off,'Inverter connected and off')

#===============================================
#Inverter connected and on
#===============================================
#figure(2)

plot_signals(time,time_no_shift,sig_inverter_con_on,filt_con_on,'Inverter connected and on')

#===============================================
#Inverter connected, on and WS=5[m/s]
#===============================================
#figure(3)

plot_signals(time,time_no_shift,sig_inverter_con_on_WS_5,filt_con_on_WS_5,'Inverter connected, on and wind speed 5 [m/s]')

#===============================================
#Inverter disconnected and off
#===============================================
#figure(4)

plot_signals(time,time_no_shift,sig_inverter_discon_off,filt_discon_off,'Inverter disconnected and off')

#===============================================
#Inverter disconnected and on
#===============================================
#figure (5)

plot_signals(time,time_no_shift,sig_inverter_discon_on,filt_discon_on,'Inverter disconnected and on')

#===============================================
#Inverter disconnected, on and WS=5[m/s]
#===============================================
#figure(6)

plot_signals(time,time_no_shift,sig_inverter_discon_on_WS_5,filt_discon_on_WS_5,'Inverter disconnected, on and Wind speed 5 [m/s]')


#%%

#Plot the original and filtered signal (no corruption) in different plots for Amplitute and 

#===============================================
#Inverter connected and off
#===============================================

plot_sep_sig(time, sig_inverter_con_off, time_no_shift, filt_con_off, 'Raw signal Inverter connected and off', 'Filtered signal Inverter connected and off', 'r')

#===============================================
#Inverter connected and on
#===============================================

plot_sep_sig(time, sig_inverter_con_on, time_no_shift, filt_con_on, 'Raw signal Inverter connected and on', 'Filtered signal Inverter connected and on', 'y')

#===============================================
#Inverter connected, on and WS=5[m/s]
#===============================================

plot_sep_sig(time, sig_inverter_con_on_WS_5, time_no_shift, filt_con_on_WS_5, 'Raw signal Inverter connected, on and wind speed 5 [m/s]', 'Filtered signal Inverter connected, on and wind speed 5 [m/s]', 'black')

#===============================================
#Inverter disconnected and off
#===============================================

plot_sep_sig(time, sig_inverter_discon_off, time_no_shift, filt_discon_off, 'Raw signal with Inverter disconnected and off', 'Filtered signal with Inverter disconnected and off', 'r-')

#===============================================
#Inverter disconnected and on
#===============================================

plot_sep_sig(time, sig_inverter_discon_on, time_no_shift, filt_discon_on, 'Raw signal with Inverter disconnected and on', 'Filtered signal with Inverter disconnected and on', 'y')

#===============================================
#Inverter disconnected, on and WS=5[m/s]
#===============================================

plot_sep_sig(time, sig_inverter_discon_on_WS_5, time_no_shift, filt_discon_on_WS_5, 'Raw signal with Inverter disconnected, on and Wind speed 5 [m/s]', 'Filtered signal with Inverter disconnected, on and Wind speed 5 [m/s]', 'black')

#////////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////

# %%

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Power spectrum plots of the signal before and after the filter is applyied
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#===============================================
#Inverter connected and off
#===============================================

f, Pxx_spec = signal.welch(sig_inverter_con_off, fs, window ='flattop', nperseg = 1024, scaling = 'spectrum')
plot_spectrum(f, Pxx_spec,'Raw signal Power spectrum (Inverter connected and off)')

# %%
#===============================================
#Inverter connected and off
#===============================================

f, Pxx_spec = signal.welch(filt_con_off, fs, window ='flattop', nperseg = 1024, scaling= 'spectrum')
plot_spectrum(f, Pxx_spec, 'Filtered signal Power spectrum (Inverter connected and off)')

#%%
#===============================================
#Inverter connected and on
#===============================================

f, Pxx_spec = signal.welch(sig_inverter_con_on, fs, window ='flattop', nperseg = 1024, scaling= 'spectrum')
plot_spectrum(f, Pxx_spec, 'Raw signal Power spectrum (Inverter connected and on)' )

# %%
#===============================================
#Inverter connected and on
#===============================================

f, Pxx_spec = signal.welch(filt_con_on, fs, window ='flattop', nperseg = 1024, scaling= 'spectrum')
plot_spectrum(f, Pxx_spec, 'Filtered signal Power spectrum (Inverter connected and on)')

#%%
#===============================================
#Inverter connected, on and WS=5[m/s]
#===============================================

f, Pxx_spec = signal.welch(sig_inverter_con_on_WS_5, fs, window ='flattop', nperseg = 1024, scaling= 'spectrum')
plot_spectrum(f, Pxx_spec, 'Raw signal Power spectrum (Inverter connected, on and WS=5m/s)')

# %%
#===============================================
#Inverter connected, on and WS=5[m/s]
#===============================================

f, Pxx_spec = signal.welch(filt_con_on_WS_5, fs, window ='flattop', nperseg = 1024, scaling= 'spectrum')
plot_spectrum(f, Pxx_spec, 'Filtered signal Power Spectrum (Inverter connected, on and WS=5m/s)')

# %%
#===============================================
#Inverter disconnected and off
#===============================================

f, Pxx_spec = signal.welch(sig_inverter_discon_off, fs, window ='flattop', nperseg = 1024, scaling = 'spectrum')
plot_spectrum(f, Pxx_spec, 'Raw signal Power spectrum (Inverter disconnected and off)')

# %%
#===============================================
#Inverter disconnected and off
#===============================================

f, Pxx_spec = signal.welch(filt_discon_off, fs, window ='flattop', nperseg = 1024, scaling= 'spectrum')
plot_spectrum(f, Pxx_spec, 'Filtered signal Power Spectrum (Inverter disconnected and off)')


#%%
#===============================================
#Inverter disconnected and on
#===============================================

f, Pxx_spec = signal.welch(sig_inverter_discon_on, fs, window ='flattop', nperseg = 1024, scaling= 'spectrum')
plot_spectrum(f, Pxx_spec, 'Raw signal Power spectrum (Inverter disconnected and on)')

#%%
#===============================================
#Inverter disconnected and on
#===============================================

f, Pxx_spec = signal.welch(filt_discon_on, fs, window ='flattop', nperseg = 1024, scaling= 'spectrum')
plot_spectrum(f, Pxx_spec, 'Filtered signal Power Spectrum (Inverter disconnected and on)')


#%%
#===============================================
#Inverter disconnected, on and WS=5[m/s]
#===============================================

f, Pxx_spec = signal.welch(sig_inverter_discon_on_WS_5, fs, window ='flattop', nperseg = 1024, scaling= 'spectrum')
plot_spectrum(f, Pxx_spec, 'Raw signal Power Spectrum (Inverter disconnected, on and WS=5m/s)')

#%%
#===============================================
#Inverter disconnected, on and WS=5[m/s]
#===============================================

f, Pxx_spec = signal.welch(filt_discon_on_WS_5, fs, window ='flattop', nperseg = 1024, scaling= 'spectrum')
plot_spectrum(f, Pxx_spec, 'Filtered signal Power Spectrum (Inverter disconnected, on and WS=5m/s)')


#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# %%
#Fourier transform for plotting the signals original and filtered in the frequency domain

#>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>
#FOR_CONNECTED_INVERTER>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>

#===============================================
#Inverter connected, off 
#===============================================

f_plot, y_input_mag_plot, y_output_mag_plot= fft_sig(sig_inverter_con_off, blank_lp_fir_con_off)
plot_FFT(f_plot, y_input_mag_plot, y_output_mag_plot, 'Blank filter output with Inverter connected, off')

#%%
#===============================================
#Inverter connected, off 
#===============================================

f_plot, y_input_mag_plot, y_output_mag_plot= fft_sig(sig_inverter_con_off, filt_con_off)
plot_FFT(f_plot, y_input_mag_plot, y_output_mag_plot, 'Not shifted filter output with Inverter connected, off')


# %%
#===============================================
#Inverter connected, on 
#===============================================

f_plot, y_input_mag_plot, y_output_mag_plot= fft_sig(sig_inverter_con_on, blank_lp_fir_con_on)
plot_FFT(f_plot, y_input_mag_plot, y_output_mag_plot, 'Blank filter output with Inverter connected, on')


#%%
#===============================================
#Inverter connected, on 
#===============================================

f_plot, y_input_mag_plot, y_output_mag_plot= fft_sig(sig_inverter_con_on, filt_con_on)
plot_FFT(f_plot, y_input_mag_plot, y_output_mag_plot, 'Not shifted filter output with Inverter connected, on')


#%%
#===============================================
#Inverter connected, on and WS=5[m/s]
#===============================================

f_plot, y_input_mag_plot, y_output_mag_plot= fft_sig(sig_inverter_con_on_WS_5, blank_lp_fir_con_on_WS_5)
plot_FFT(f_plot, y_input_mag_plot, y_output_mag_plot, 'Blank filter output with Inverter connected, on and WS=5[m/s]')


#%%
#===============================================
#Inverter connected, on and WS=5[m/s]
#===============================================

f_plot, y_input_mag_plot, y_output_mag_plot= fft_sig(sig_inverter_con_on_WS_5, filt_con_on_WS_5) 
plot_FFT(f_plot, y_input_mag_plot, y_output_mag_plot, 'Not shifted filter output with Inverter connected, on and WS=5[m/s]')


# %%

#>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>
#FOR_DISCONNECTED_INVERTER>> 
#>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>

#===============================================
#Inverter disconnected, off 
#===============================================

f_plot, y_input_mag_plot, y_output_mag_plot= fft_sig(sig_inverter_discon_off, blank_lp_fir_discon_off)
plot_FFT(f_plot, y_input_mag_plot, y_output_mag_plot, 'Blank filter output with Inverter disconnected, off')


#%%
#===============================================
#Inverter disconnected, off 
#===============================================

f_plot, y_input_mag_plot, y_output_mag_plot= fft_sig(sig_inverter_discon_off, filt_discon_off)
plot_FFT(f_plot, y_input_mag_plot, y_output_mag_plot, 'Not shifted filter output with Inverter disconnected, off')


# %%
#===============================================
#Inverter disconnected, on 
#===============================================

f_plot, y_input_mag_plot, y_output_mag_plot= fft_sig(sig_inverter_discon_on, blank_lp_fir_discon_on)
plot_FFT(f_plot, y_input_mag_plot, y_output_mag_plot, 'Blank filter output with Inverter disconnected, on')


#%%
#===============================================
#Inverter disconnected, on 
#===============================================

f_plot, y_input_mag_plot, y_output_mag_plot= fft_sig(sig_inverter_discon_on, filt_discon_on)
plot_FFT(f_plot, y_input_mag_plot, y_output_mag_plot, 'Not shifted filter output with Inverter disconnected, on')


#%%
#===============================================
#Inverter disconnected, on and WS=5[m/s]
#===============================================

f_plot, y_input_mag_plot, y_output_mag_plot= fft_sig(sig_inverter_discon_on_WS_5, blank_lp_fir_discon_on_WS_5)
plot_FFT(f_plot, y_input_mag_plot, y_output_mag_plot, 'Blank filter output with Inverter disconnected, on and WS=5[m/s]')


#%%
#===============================================
#Inverter disconnected, on and WS=5[m/s]
#===============================================

f_plot, y_input_mag_plot, y_output_mag_plot= fft_sig(sig_inverter_discon_on_WS_5, filt_discon_on_WS_5)
plot_FFT(f_plot, y_input_mag_plot, y_output_mag_plot, 'Not shifted filter output with Inverter disconnected, on and WS=5[m/s]')


#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# %%

# %%
