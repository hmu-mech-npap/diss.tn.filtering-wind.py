# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import numpy as np 
import math
import matplotlib.pyplot as plt
from scipy import signal

# 4TH ORDER BUTTERWORTH FILTER WITH A GAIN DROP OF 1/sqrt(2) AT 0.4 CYCLES/SAMPLE
bb, ab  = signal.butter (N = 10,Wn = 0.8, btype= 'low', analog=False, output='ba')
print ('Coefficients of b = ', bb)
print ('Coefficients of a = ', ab)
wb, hb = signal.freqz(bb, ab, worN = 512, whole = False, include_nyquist = True) # adding "include_nyquist = True" plots the last frequency that is otherwise ignored if "worN = int" && "whole = False" 
wb = wb/(2*math.pi)
plt.plot(wb, abs(np.array(hb)))  

plt.title('Butterworth filter frequency response')
plt.xlabel('Frequency [cycles/sample]')
plt.ylabel('Amplitute [dB]')
plt.margins(0, 0.1)
plt.grid(which = 'both', axis='both')



# %%
# 4TH ORDER BESSEL FILTER WITH A GAIN DROP OF 1/sqrt(2) AT 0.4 CYCLES/SAMPLE

bb_1, ab_1 = signal.bessel (N = 4, Wn = 0.8, btype = 'low', analog=False, output='ba')
print ('Coefficients of b = ', bb_1)
print ('Coefficients of a = ', ab_1)
wb_1, hb_1 = signal.freqz(bb_1, ab_1, worN = 512, whole = False, include_nyquist = True)
wb_1 = wb_1/(2*math.pi)
plt.plot(wb_1, abs(np.array(hb_1)))

plt.title('Bessel filter frequency response')
plt.xlabel('Frequency [cycles/sample]')
plt.ylabel('Amplitute [dB]')
plt.margins(0, 0.1)
plt.grid(which= 'both', axis= 'both')

# %%
#4TH ORDER CHEBYSHEV FILTER TYPE 1 (ONLY IN PASSBAND RIPPLES) WITH MAX RIPPLES=2 AND THE GAIN DROP AT 1.5 CYCLES/SAMPLE

bb_2, ab_2 = signal.cheby1 (N = 20, rp = 2, Wn = 0.2, btype = 'low', analog=True, output='ba')
print ('Coefficients of b = ', bb_2)
print ('Coefficients of a = ', ab_2)
wb_2, hb_2 = signal.freqz(bb_2, ab_2, worN = 512, whole = False, include_nyquist = True)
wb_2 = wb_2/(2*math.pi)
plt.plot(wb_2, abs(np.array(hb_2)))
plt.title('Chebyshev filter frequency response')
plt.xlabel('Frequency [cycles/sample]')
plt.ylabel('Amplitute [dB]')
#plt.margins(0, 0.1)
plt.grid(which= 'both', axis= 'both')

# %%
# 4TH ORDER ELLIPTIC FILTER WITH MAX RIPPLES =2dB IN PASSBAND, MIN ATTENUATION =8dB IN STOP BAND AT 0.25 CYCLES/SAMPLE

bb_3, ab_3 = signal.ellip (N = 4, rp = 2, rs = 8, Wn = 0.5, btype = 'low', analog=False, output='ba')
print ('Coefficients of b = ', bb_3)
print ('Coefficients of a = ', ab_3)
wb_3, hb_3 = signal.freqz(bb_3, ab_3, worN = 512, whole = False, include_nyquist = True)
wb_3 = wb_3/(2*math.pi)
plt.plot(wb_3, abs(np.array(hb_3)))

plt.title('Elliptic filter frequency response')
plt.xlabel('Frequency [cycles/sample]')
plt.ylabel('Amplitute [dB]')
plt.margins(0, 0.1)
plt.grid(which= 'both', axis= 'both')







# %%
