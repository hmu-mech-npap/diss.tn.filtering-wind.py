#%% [markdown]
# # scope
# To understand difference in parameters in welch and fft.   
#
#%%
import numpy as np
from numpy.fft import fft, ifft
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn-poster')
#%matplotlib inline
#%% setup signal
# sampling rate
sr = 2000
# sampling interval
ts = 1/sr
t = np.arange(0,10,ts)

freq = 1.
x = 3*np.sin(2*np.pi*freq*t)

freq = 4
x += np.sin(2*np.pi*freq*t)

freq = 7   
x += 0.5* np.sin(2*np.pi*freq*t)

X = fft(x)
N = len(X)
n = np.arange(N)
T = N/sr
freq = n/T 
#%%

plt.figure(figsize = (12, 6))
plt.subplot(121)

# plt.loglog(freq, np.abs(X), 'b')
plt.plot(freq, np.abs(X), 'b.')
plt.xlabel('Freq (Hz)')
plt.ylabel('FFT Amplitude |X(freq)|')
plt.xlim(0, 10)

plt.subplot(122)
plt.plot(t, ifft(X), 'r')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.tight_layout()
plt.show()
# %%
import scipy.signal as signal
# %%
f, Pxx_den = signal.welch(x, fs=sr,nperseg=1000<<7, scaling='density')
plt.figure(figsize = (12, 6))
plt.subplot(121)

# plt.loglog(freq, np.abs(X), 'b')
plt.plot(freq, np.abs(X), 'b.')
plt.xlabel('Freq (Hz)')
plt.ylabel('FFT Amplitude |X(freq)|')
plt.xlim(0, 10)

plt.subplot(122)
plt.plot(f, Pxx_den, 'r.-')
plt.xlabel('Freq (Hz)')
plt.ylabel('Power')
plt.tight_layout()
plt.xlim(0, 10)

plt.show()

# %%
# Some plot standards
plt.rcParams ['figure.figsize'] =[16,12]
plt.rcParams.update ({'font.size': 18})

n= len(t)
fhat = fft(x,n)                              # compute fft
PSD = fhat * np.conj(fhat) / n               # Power spectrum (power/freq)
freq = (1/(ts*n)) * np.arange(n)             # create x-axis (frequencies)
L = np.arange(1,np.floor(n/2),dtype=int)     # plot only first half (possitive

fig, axs = plt.subplots(2,1)

plt.sca(axs[0])
plt.plot(t,x)

plt.sca(axs[1])
plt.plot(freq[L],PSD[L])
plt.xlim(0,10)
plt.show()
#this is a version that uses the new package pros_noisefiltering
# %%
