# %%
#Apllying a filter on a sinusoidal signal with  noise at 8000 Hz and retrieving the pure sinusoidal tone of the sum of sin waves 10 Hz and 20 Hz 
from cProfile import label
import numpy as np
from numpy import logspace
import matplotlib.pyplot as plt
from scipy import signal

#define a function for plotting the Frequency response of the filter
def plot_response(fs, w, h, title):
    plt.figure()
    plt.plot(0.5*fs*w/np.pi, 20*np.log10(np.abs(h)))
    plt.ylim(-40, 5)
    #plt.xlim(0, 0.5*fs)
    plt.xscale('log')
   
    plt.grid(True)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Gain (dB)')
    plt.title(title)

#Generate a signal for filtering
def generate_random_signal():
    t= np.linspace(0, 1, 44000, False) # 1 sec
    f0= 10
    sig = 2* np.sin(2*np.pi*f0*t) + 3* np.sin(2*np.pi*2*f0*t) + 8* np.sin(2*np.pi*800*f0*t)           #np.random.rand(t.shape[0]
    return (t, sig)
t, sig = generate_random_signal()

# IIR Low-pass Butterworth filter response on the signal
sos = signal.butter(N = 10, Wn = 3250, btype = 'lp', fs = 44000, output = 'sos')
filtered = signal.sosfilt(sos, sig)
fig, (ax1, ax2) = plt.subplots( 2, 1, sharex=True)
ax1.plot(t, sig)
ax1.set_title('10 and 20 Hz sinusoids with 8kHz interferences')
ax1.axis([0, 1, -15, 15])
ax2.plot(t, filtered)
ax2.set_title('After Filtering the 8kHz with IIR Butterworth filter')
ax2.axis([0, 1, -5, 5])
ax2.set_xlabel('Time [seconds]')
plt.tight_layout()
plt.show()

# Seperate of 10 Hz and 20 Hz signals using IIR Butterworth LP and HP for seperation
sos_lp_2=signal.butter(N = 10, Wn = 15, btype = 'lowpass', fs = 44000, output = 'sos')
sos_hp_2=signal.butter(N = 10, Wn = 15, btype = 'highpass', fs = 44000, output = 'sos')
filtered_lp_2= signal.sosfilt(sos_lp_2, filtered)
filtered_hp_2= signal.sosfilt(sos_hp_2,filtered)
fig, (ax1, ax2) = plt.subplots( 2, 1, sharex=True)
ax1.plot(t, filtered)
ax1.set_title('filtered signal of 10 and 20 Hz sinusoids using IIR Butterworth filter')
ax1.axis([0, 1, -5, 5])
ax2.plot(t, filtered_lp_2, label='10 Hz')
ax2.plot(t,filtered_hp_2, label=('20 Hz'))
ax2.axis([0, 1, -4, 4])
ax2.set_xlabel('Time [seconds]')
plt.tight_layout()
plt.legend(bbox_to_anchor =(0.70, 1.15), ncol = 2 )
plt.show()


# FIR Low-pass filter 
fs = 44000        #sampling freq
cutoff = 3250     #Cutoff freq for gain drop
trans_width = 250 # width of transition from passband to stopband in Hz
numtaps = 200     #Size of the FIR filter

#Construct a Low-pass FIR filter 
taps = signal.remez(numtaps, [0, cutoff, cutoff+trans_width, 0.5*fs], [1,0], Hz= fs)
w, h = signal.freqz(taps, [1], worN=2000)

#Applying the FIR LP filter to the signal 
y = signal.lfilter(taps, 1.0, sig)
fig, (ax1, ax2) = plt.subplots( 2, 1, sharex=True)
ax1.plot(t, sig)
ax1.set_title('10 and 20 Hz sinusoids with 8kHz interferences')
ax1.axis([0, 1, -15, 15])
ax2.plot(t, y)
ax2.set_title('After Filtering the 8kHz with FIR filter (signal.remez)')
ax2.axis([0, 1, -5, 5])
ax2.set_xlabel('Time [seconds]')
plt.tight_layout()
plt.show()

#Plot the frequency response of the FIR Low-pass (Filter signal.remez)
plot_response(fs, w, h, "FIR Low-pass (Filter signal.remez)")

#Construct a Low-pass FIR LP filter with Kaiser Window method
nyq_rate = fs/2.0
width = 8/nyq_rate
ripple_dB = 10
N, beta = signal.kaiserord(ripple_dB, width)
cutoff_hz = cutoff

taps_2 = signal.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
w_2, h_2 = signal.freqz(taps_2, [1], worN=2000)
y_2 = signal.lfilter(taps_2, 1.0, sig)


fig, (ax1, ax2) = plt.subplots( 2, 1, sharex=True)
ax1.plot(t, sig)
ax1.set_title('10 and 20 Hz sinusoids with 8kHz interferences')
ax1.axis([0, 1, -15, 15])
ax2.plot(t, y_2)
ax2.set_title('After Filtering the 8kHz with FIR LP filter(kaiser window signal.firwin)')
ax2.axis([0, 1, -5, 5])
ax2.set_xlabel('Time [seconds]')
plt.tight_layout()
plt.show()

plot_response(fs, w_2, h_2, "FIR Low-pass filter (signal.firwin (kaiser))")


#Construct a FIR BP filter with kaiser window method
f1, f2= 1/nyq_rate, 15/nyq_rate

taps_2_bandpass_kaiser = signal.firwin(numtaps, [f1, f2], pass_zero=False)
w_2_bp_kaiser,h_2_bp_kaiser = signal.freqz(taps_2_bandpass_kaiser, [1], worN=2000) 
y_2_bp_kaiser = signal.lfilter(taps_2_bandpass_kaiser, 1.0, sig)

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
ax1.plot(t, sig)
ax1.set_title('10 and 20 Hz sinusoids with 8kHz interferences')
ax1.axis([0, 1, -15, 15])
ax2.plot(t, y_2_bp_kaiser)
ax2.set_title('After Filtering the 8kHz with FIR BP filter(kaiser window signal.firwin)')
plt.tight_layout()
plt.show()

#Plot the frequency response of BP FIR filter (kaiser window method)
plot_response(fs, w_2_bp_kaiser, h_2_bp_kaiser, "FIR Band-pass filter (signal.firwin (kaiser))")


#Seperate of 10 Hz and 20 Hz signals using FIR LP and HP for seperation
cutoff_2 = 10
cutoff_2_hp = 44
trans_width_2 = 1
numtaps_2 = 8000

#Construct a Low-pass FIR filter 
taps_2_lp = signal.remez(numtaps_2, [0, cutoff_2, cutoff_2+trans_width_2, 0.5*fs], [1,0], Hz= fs)
w_2_lp, h_2_lp = signal.freqz(taps_2_lp, [1], worN=2000)

#Construct a High-pass FIR filter 
taps_2_hp = signal.remez(numtaps_2, [0, cutoff_2_hp-trans_width_2, cutoff_2_hp, 0.5*fs], [0,1], Hz= fs)
w_2_hp, h_2_hp = signal.freqz(taps_2_hp, [1], worN=2000)

#Apply the FIR HP and LP filters
y_2_lp = signal.lfilter(taps_2_lp, 1.0, y)
y_2_hp = signal.lfilter(taps_2_hp, 1.0, y)

#Plot the 2 signals seperate
fig, (ax1, ax2)= plt.subplots(2, 1, sharex=True)
ax1.plot(t, y_2_hp)
ax1.set_title('20 Hz sine wave')
ax1.axis([0, 1, -6, 6])
ax2.plot (t, y_2_lp)
ax2.set_title('10 Hz sine wave')
ax2.axis([0, 1, -6, 6])
plt.tight_layout()
plt.show()


"""
#Construct a Bandpass filter to seperate 10 and 20 Hz
#Band pass filter from 1 to 16 Hz
band = [2,12]
numtaps_bandpass = 1000
edges = [0, band[0] - trans_width_2, band[0], band[1], band[1] + trans_width_2, 0.5*fs]
taps_bandpass_10_Hz = signal.remez(numtaps_bandpass, edges, [0, 1, 0], Hz=fs)
w_bp_10_Hz, h_bp_10_Hz = signal.freqz(taps_bandpass_10_Hz, [1], worN=2000)

band_pass_for_10_Hz = signal.lfilter(taps_bandpass_10_Hz, 1.0, y)

#Band pass filter from 16 to 100 Hz
band_2 = [15, 50]
edges_2 = [0, band_2[0] - trans_width_2, band_2[0], band_2[1], band_2[1] + trans_width_2, 0.5*fs]
taps_bandpass_20_Hz = signal.remez(numtaps_bandpass, edges_2, [0, 1, 0], Hz=fs)
w_bp_20_Hz, h_bp_20_Hz = signal.freqz(taps_bandpass_20_Hz, [1], worN=2000)
band_pass_for_20_Hz = signal.lfilter(taps_bandpass_20_Hz, 1.0, y)

#Plot the 2 signals seperate
fig, (ax1, ax2)= plt.subplots(2, 1, sharex=True)
ax1.plot(t, band_pass_for_20_Hz)
ax1.set_title('20 Hz sine wave')
ax1.axis([0, 1, -6, 6])
ax2.plot (t, band_pass_for_10_Hz)
ax2.set_title('10 Hz sine wave')
ax2.axis([0, 1, -6, 6])
plt.tight_layout()
plt.show()

"""

#Plot the Frequency response of the filter

plot_response(fs, w_2_hp, h_2_hp, "FIR High-pass Filter")
plot_response(fs, w_2_lp, h_2_lp, "FIR Low-pass Filter")
#plot_response(fs, w_bp_10_Hz, h_bp_10_Hz, "FIR Band-pass Filter 10 Hz")
#plot_response(fs, w_bp_20_Hz, h_bp_20_Hz, "FIR Band-pass Filter 20 Hz")


# %%
# Power Spectrum / signal.welch
fs = 44000
f, Pxx_spec = signal.welch(sig, fs, window ='flattop', nperseg = 1024, scaling = 'spectrum')
plt.figure()
plt.semilogy(f, np.sqrt(Pxx_spec))
plt.xlim(0, 10000)

plt.xlabel('Frequency [Hz]')
plt.ylabel('Linear spectrum [V RMS]')
plt.title('Power spectrum before filter is applied')
plt.show()

# %%
#IIR Butterworth filtered signal Power Spectrum
fs = 44000
f, Pxx_spec = signal.welch(filtered, fs, window ='flattop', nperseg = 1024, scaling= 'spectrum')
plt.figure()
plt.semilogy(f, np.sqrt(Pxx_spec))
plt.xlim(0,10000)
plt.xlabel ('Frequency [Hz]')
plt.ylabel ('Linear Spectrum [V RMS]')
plt.title (' IIR Butterworth LP filtered signal Power Spectrum')
plt.show ()

# %%
#FIR filtered signal Power Spectrum 
fs = 44000
f, Pxx_spec = signal.welch(y, fs, window ='flattop', nperseg = 1024, scaling= 'spectrum')
plt.figure()
plt.semilogy(f, np.sqrt(Pxx_spec))
plt.xlim(0,10000)
plt.xlabel ('Frequency [Hz]')
plt.ylabel ('Linear Spectrum [V RMS]')
plt.title (' FIR LP filtered signal Power Spectrum')
plt.show ()

#%%

# simulation of the system response to the butterworth filter used to eliminate noise
from scipy.signal import lsim
b, a = signal.butter(N=20, Wn=2*np.pi*3250, btype='lowpass',fs=44000, analog=False)
tout, yout, xout = lsim((b, a), U=sig, T=t)
plt.plot (t, sig, 'r', alpha=0.5, linewidth=1, label='input')
plt.plot (tout, yout, 'k', alpha = 1, linewidth=1, label='output')
plt.legend (loc='best', shadow=False, framealpha=1)
plt.grid (alpha=0.5)
plt.xlabel ('time')
plt.show ()

# %%
# Fast Fourier Transformation of input and output signals 
f0=10
N = int(10*(fs/f0))   

yf_input = np.fft.rfft(sig) 
y_input_mag_plot = np.abs(yf_input)/N


f= np.linspace (0, (N-1)*(fs/N),N )

f_plot = f[0:int(N/2+1)]
y_input_mag_plot = 2*y_input_mag_plot[0:int(N/2+1)]
y_input_mag_plot[0] = y_input_mag_plot[0] / 2

fig, (ax1, ax2) = plt.subplots(2,1, sharex=True)
fig.suptitle('IIR butterworth Low-pass Filter')
ax1.plot(f_plot, y_input_mag_plot)
ax1.grid(alpha=0.3)

ax1.set_ylabel('Amplitute [dB]')

yf_output = np.fft.rfft(filtered)
y_output_mag_plot = np.abs(yf_output)/N
y_output_mag_plot = 2* y_output_mag_plot[0:int(N/2+1)]
y_output_mag_plot[0]= y_output_mag_plot[0]/2  
ax2.plot(f_plot, y_output_mag_plot)

plt.plot(f_plot, y_output_mag_plot, label='output signal')
plt.grid(alpha=0.3)
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitute [dB]')
plt.xscale('log')
plt.legend()

plt.show()

#Plot the signal in frequency domain after using FIR LP (signal.remez) 
fig, (ax1, ax2) = plt.subplots(2,1, sharex=True)
fig.suptitle('FIR Low-pass Filter (signal.remez)')
ax1.plot(f_plot, y_input_mag_plot, label= 'input signal')
ax1.grid(alpha=0.3)

ax1.set_ylabel('Amplitute [dB]')

yf_output = np.fft.rfft(y)
y_output_mag_plot = np.abs(yf_output)/N
y_output_mag_plot = 2* y_output_mag_plot[0:int(N/2+1)]
y_output_mag_plot[0]= y_output_mag_plot[0]/2  
ax2.plot(f_plot, y_output_mag_plot)

plt.plot(f_plot, y_output_mag_plot, label= 'output signal')
plt.grid(alpha=0.3)
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitute [dB]')
plt.xscale('log')
plt.legend()

plt.show()

#Plot the signal in frequency domain after using FIR LP kaiser window method 
fig, (ax1, ax2) = plt.subplots(2,1, sharex=True)
fig.suptitle('FIR Low-pass Kaiser Window method')
ax1.plot(f_plot, y_input_mag_plot, label='input signal')
ax1.grid(alpha=0.3)

ax1.set_ylabel('Amplitute [dB]')

yf_output = np.fft.rfft(y_2)
y_output_mag_plot = np.abs(yf_output)/N
y_output_mag_plot = 2* y_output_mag_plot[0:int(N/2+1)]
y_output_mag_plot[0]= y_output_mag_plot[0]/2  
ax2.plot(f_plot, y_output_mag_plot)

plt.plot(f_plot, y_output_mag_plot, label= 'output signal')
plt.grid(alpha=0.3)
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitute [dB]')
plt.xscale('log')
plt.legend()

plt.show()



# %%
#Bode plot for input and output
# needs more work for proper implementation
H= yf_output/ yf_input
Y = np.imag (H)
X = np.real (H)
#Mag_of_H = 20*cmath.log10(Y)
f = logspace(-1,0.001) # frequencies from 0 to 10**5
sys = signal.lti([H],f)
w, mag, phase = signal.bode(sys, n= f)
#print (w, mag, phase)
plt.plot(f, w, label= 'Frequency rad/sec')
plt.plot(f, mag, label= 'Magnitude [dB]' )
plt.plot(f, phase, label='Phase array [deg]' )
plt.grid(which='both', axis= 'both') 
plt.legend()       
#plt.xlabel('Real numbers R')
#plt.ylabel('Imaginary numbers I')
#plt.scatter(X,Y)


#plt.show()

#fig= plt.figure()
#ax = fig.add_subplot(projection = 'polar')
#c= ax.scatter(X,Y)
#plt.title('Polar representation of ')