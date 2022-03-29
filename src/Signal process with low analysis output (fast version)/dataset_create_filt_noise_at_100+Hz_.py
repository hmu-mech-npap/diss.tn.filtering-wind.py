#%%

import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt


file_path = input('The full path of raw data file to process: ' )
file_name_of_raw =input('Enter the name of the raw signal file :') 

#Read and store the .h5 file with pandas
f_1 = pd.HDFStore(path=f'{file_path}{file_name_of_raw}', mode='r')

print('The data frame key is: ',f_1.keys())

data_fr_key = input('Input the data frame key of raw signal file:' )

data_raw = f_1[data_fr_key]
print(data_raw.info())

L = list(data_raw.keys())

print (L)


i=0
raw_file = []
for i in range (0,len(L)):
    raw_file.append(data_raw.get(L[i]))
    i+=1
i=0
first_sig_raw_col_ = raw_file[0]

sig_in_numpy_format = []
for i in range (0, len(L) ):
    sig_in_numpy_format.append(np.array(raw_file[i]))
    i+=1
i=0


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

#Apply the filter to the signal column by column from the data set

blank_lp_fir_con_off = signal.lfilter(fir_co, 1.0, sig_in_numpy_format[0])


blank_lp_fir_con_on = signal.lfilter(fir_co, 1.0, sig_in_numpy_format[1])

blank_lp_fir_con_on_WS_5 = signal.lfilter(fir_co, 1.0, sig_in_numpy_format[2])

blank_lp_fir_discon_off = signal.lfilter(fir_co, 1.0, sig_in_numpy_format[3])

blank_lp_fir_discon_on = signal.lfilter(fir_co, 1.0, sig_in_numpy_format[4])

blank_lp_fir_discon_on_WS_5 = signal.lfilter(fir_co, 1.0, sig_in_numpy_format[5])

#=====================================================
#++++++++ Plot original and filtered signal+++++++++++ 
#=====================================================

#Time interval of the samples
time = np.linspace(0, 7.599998, len(data_raw))

#The first N-1 samples are corrupted by the initial conditions
warmup = numtaps_2 - 1

#The phase delay of the filtered signal
delay= (warmup / 2) / fs

time_no_shift = time[warmup:]-delay


# signal shift for rejecting the corrupted signal from the 
#blank output of the filter

filt_con_off  = blank_lp_fir_con_off[warmup:]

filt_con_on = blank_lp_fir_con_on[warmup:]

filt_con_on_WS_5 = blank_lp_fir_con_on_WS_5[warmup:]

filt_discon_off = blank_lp_fir_discon_off[warmup:]

filt_discon_on = blank_lp_fir_discon_on[warmup:]

filt_discon_on_WS_5 = blank_lp_fir_discon_on_WS_5[warmup:]


#Construct data frame better 
#using pandas library

#Rename old attributes to mach with filtered data
#signal

F = []
for i in range(0,len(L)):
    F.append(L[i].replace("raw","filt"))
i=0

#Create the new file
#Choose the desired directory to create the new file 
#and add the __NAME__.h5 at the end of the screen 
# WARNING : If file already exists in the dir and it is closed via :
#hf_st_pd_.close() it will be overwritten
final_data = [filt_con_off, filt_con_on, filt_con_on_WS_5, filt_discon_off,filt_discon_on,filt_discon_on_WS_5]


new_file_name = input("""Enter the name of the new folder : 
the file will be created in the same path with the raw data file
if 0 is passed for a new name the old name is used with replacing
the "raw" at the end of the name with "filt"
""")

if new_file_name == '0' :
    file_name = file_name_of_raw.replace("raw", "filt")
else:
    file_name = new_file_name

hf_st_pd_ = pd.HDFStore(f'{file_path}{file_name}', mode='w')

df2 = pd.DataFrame({
        
    F[0]:final_data[0],
    F[1]:final_data[1],
    F[2]:final_data[2],
    F[3]:final_data[3],
    F[4]:final_data[4],
    F[5]:final_data[5]
    }
,index=(time_no_shift)
)

hf_st_pd_.put('df_filt', df2, format='table', data_columns=True)
    
hf_st_pd_.close()


#%%
#Read the file that was just created

f_3 = pd.HDFStore(path=f'{file_path}{file_name}',mode='r')

data_filt = f_3['df_filt']
# %%
#This is added in order to avoid manual close of the filtered data file
f_3.close()

