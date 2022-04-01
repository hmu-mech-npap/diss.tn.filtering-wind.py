#%%

import numpy as np
import pandas as pd
from scipy import signal

#%%
file_path = input('The full path of raw data file to process: ' )
file_name_of_raw =input('Enter the name of the raw signal file :') 
#%%
#Read and store the .h5 file with pandas
f_1 = pd.HDFStore(path=f'{file_path}{file_name_of_raw}', mode='r')

print('The data frame key is: ',f_1.keys())

data_fr_key = input('Input the data frame key of raw signal file:' )

data_raw = f_1[data_fr_key]
L = list(data_raw.keys())

print(data_raw.info())
#%%
#Extract the raw data from the folder for processing
raw_sig_df =[]

for element1 in L:
    raw_sig_df.append(data_raw.get(element1))

sig_array= []
for element2 in raw_sig_df:
    sig_array.append(np.array(element2))

#%%
#The only filter with les standard deviation on output from input

#FIR Low-pass filter on the signal with the inverter connected and off

#The length of the filter(number of coefficients, the filter order + 1)
numtaps_2 = 100_000
fs = 500_000
cutoff_hz = 0.00001
nyq_rate = fs/2 

#Use of firwin to create low-pass FIR filter
fir_co = signal.firwin(numtaps_2, cutoff_hz)
w_fir_co, h_fir_co = signal.freqz(fir_co, [1])

#%%
# LET'S MAKE IT BETTER
blank_output =[]
experiment = []
for element3 in sig_array:
    blank_output = signal.lfilter(fir_co, 1.0, element3)
    experiment.append(blank_output)

#%%

#=====================================================
#++++++++ Plot original and filtered signal+++++++++++ 
#=====================================================
#%%
#Time interval of the samples
time = np.linspace(0, 7.599998, len(data_raw))

#The first N-1 samples are corrupted by the initial conditions
warmup = numtaps_2 - 1

#The phase delay of the filtered signal
delay= (warmup / 2) / fs

time_no_shift = time[warmup:]-delay


#%%
# signal shift for rejecting the corrupted signal from the 
#blank output of the filter


filt_data = []
for element4 in experiment:
    filt_data.append(element4[warmup:])


#%%
#Construct data frame better 
#using pandas library

#Rename old attributes to mach with filtered data
#signal

F = []
for i in range(0,len(L)):
    F.append(L[i].replace("raw","HD"))
i=0

#%%
#Create a dictionary from the lists of modified keys and filtered output 
a = dict(zip(F, filt_data))
#Create a pandas dataframe for the generated file 
df=pd.DataFrame(data=a, index=None)
df.insert(loc=0, column="Time", value=time_no_shift)

#%%
#Create the new file
#Choose the desired directory to create the new file 
#and add the __NAME__.h5 at the end of the screen 
# WARNING : If file already exists in the dir and it is closed via :
#hf_st_pd_.close() it will be overwritten

#%%
new_file_name = input("""Enter the name of the new file : 
the file will be created in the same path folder with the raw data 
if 0 is passed for a new name the old name is used with replacing
the "raw" at the start of the name with "HD"
""")

if new_file_name == '0' :
    file_name = file_name_of_raw.replace("raw", "HD")
else:
    file_name = new_file_name

#HDF5 file in same path with raw signal folder diff name
hf_st_pd_ = pd.HDFStore(f'{file_path}{file_name}', mode='w')
hf_st_pd_.put('df', df, format='table', data_columns=True)
hf_st_pd_.close()
#%%
#Read the file that was just created

f_3 = pd.HDFStore(path=f'{file_path}{file_name}',mode='r')

data_filt = f_3['df']
# %%
#This is added in order to avoid manual close of the filtered data file
f_3.close()
