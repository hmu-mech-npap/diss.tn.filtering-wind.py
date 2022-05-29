# %%
#Use of pandas library for reading hdf5 file format
from functions import (Axis_titles, Graph_data_container, Signals_for_fft_plot,
                        Time_domain_data_cont, Fft_Plot_info, fft_calc_sig,
                        plot_signals, 
                        plot_spect_comb2, spect,
                        fft_sig, plot_FFT,
                        )

from lp_firwin_method_ import lp_firwin, filt_sig
from file_import_ import data_import
from pathlib import Path

#Constants
FS = 500_000

DATA_FOLDER_HDF5 = Path.cwd()
PROCESS_TYPE = 'raw'
file_name = f'/noise_reference_{PROCESS_TYPE}.h5'

# Import the file for process
RAW_DATA_ALL, raw_keys, CHUNKED_DATA = data_import(file_path=DATA_FOLDER_HDF5, file_name_of_raw=file_name)

# Construct the desiered FIR filter
filter_coeff, w, h = lp_firwin(numtaps_2=20, FS=FS, cutoff_Hz=0.0001)

#filtering of the fignal with the above filter coefficients
Filt, Blank, chunked_time, TIME_NO_SHIFT=filt_sig(coeff=filter_coeff, order=20,
                                                    FS=FS, Raw=CHUNKED_DATA
                                                )

# Seperate the information for the signal in 3 independent functions for later import 
# from the application and also not overfeed the user.

# Plotting the raw and filtered signals in time domain combined  for comparison 
def plot_signals_time_domain():   
    for element in range(6):
        plot_signals([Time_domain_data_cont(chunked_time,CHUNKED_DATA[element],
                                            label='Raw signal old data'),
                     Time_domain_data_cont(TIME_NO_SHIFT,Filt[element],
                                            label='FIR filtering old data'),    ],
                    [Axis_titles('Time [s]','Amplitude [dB]')],
                    Title=Titles[element],
                    figsize=(10,6))

# Plotting the power spectral density of the signals in the same manner
def plot_signals_psd():
    #Plot the raw and filtered signals power spectrums with titles 
    for i,j,t in zip(CHUNKED_DATA, Filt, range(6)):
        f_r, Prr_spec = spect(i,FS=FS)
        f_f, Pff_spec = spect(j,FS=FS)
        plot_spect_comb2([Graph_data_container(f_r,Prr_spec,
                                                label='Raw signal'),
                          Graph_data_container(f_f,Pff_spec,
                                                label='FIR filtered old data')     ],
                        title=Titles[t],
                        Kolmogorov_offset=1e3,
                        xlim=[1e1,1e5],
                        figsize=(10,6))

# FFT plots
def plot_fft_freq_domain():
    #Compute the FFT of raw, corrupted and uncorrupted signals and plot them combined in pairs for comparison 
    for element in range(6):

        f_sh,yin_sh,yout_sh =fft_sig([fft_calc_sig(CHUNKED_DATA[element],Filt[element], None)])
        
        
        plot_FFT([Signals_for_fft_plot(f_sh, yin_sh, yout_sh)   ],
                [Fft_Plot_info(Titles[element],'FIR','Uncorrupted')],
                [Axis_titles('Frequency [Hz]','Amplitude [dB]')],
                figsize=(10,6))


# %%
if __name__=='__main__':
    #Plot of the raw and filtered signals in one graph with different colors for 
    #better understanding the response of the filter at the system in time domain
    Titles = [  'Inverter connected and off','Inverter connected and on',
                'Inverter connected, on and wind speed 5 [m/s]',
                
                'Inverter disconnected and off','Inverter disconnected and on',
                'Inverter disconnected, on and Wind speed 5 [m/s]']
    #plot_fft_freq_domain()
    #plot_signals_time_domain()
    plot_signals_psd()



# %%
