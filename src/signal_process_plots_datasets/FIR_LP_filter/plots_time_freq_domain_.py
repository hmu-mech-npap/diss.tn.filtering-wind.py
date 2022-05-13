# %%
#Use of pandas library for reading hdf5 file format
from functions import plot_signals, plot_sep_sig, spect, plot_spectrum, fft_sig, plot_FFT, plot_response
from lp_firwin_method_ import lp_firwin, filt_sig
from file_import_ import data_import

# Import the file for process
RAW_DATA_ALL, raw_keys, CHUNKED_DATA = data_import(file_path='/home/goodvibrations32/Documents/Git_clones_dissertation/diss.tn.filtering-wind.py/src/signal_process_plots_datasets/FIR_LP_filter/', file_name_of_raw='noise_reference_raw.h5')

# Construct the desiered FIR filter
filter_coeff, w, h = lp_firwin(numtaps_2=20, FS=500_000, cutoff_Hz=0.0001)

#filtering of the fignal with the above filter coefficients
Filt, Blank, chunked_time, TIME_NO_SHIFT=filt_sig(coeff=filter_coeff, order=20, FS=500_000, Raw=CHUNKED_DATA)

if __name__=='__main__':

    #Plot of the raw and filtered signals in one graph with different colors for 
    #better understanding the response of the filter at the system in time domain
    Titles = ['Inverter connected and off','Inverter connected and on','Inverter connected, on and wind speed 5 [m/s]','Inverter disconnected and off','Inverter disconnected and on','Inverter disconnected, on and Wind speed 5 [m/s]']

    # for simultaneously looping through lists
    #a list with titles discribing the system condition (connected inverter or not etc.).

    for i,j,k in zip(CHUNKED_DATA, Filt, Titles):
        plot_signals(chunked_time,TIME_NO_SHIFT,i,j,k)
    
    #List the titles and colores that are to be plotted
    raw_titles = ['Raw signal Inverter connected and off','Raw signal Inverter connected and on','Raw signal Inverter connected, on and wind speed 5 [m/s]','Raw signal with Inverter disconnected and off','Raw signal with Inverter disconnected and on','Raw signal with Inverter disconnected, on and Wind speed 5 [m/s]']
    filt_titles = ['Filtered signal Inverter connected and off','Filtered signal Inverter connected and on','Filtered signal Inverter connected, on and wind speed 5 [m/s]','Filtered signal with Inverter disconnected and off','Filtered signal with Inverter disconnected and on','Filtered signal with Inverter disconnected, on and Wind speed 5 [m/s]']
    colors_filt = ['r','y','black','r','y','black']
    
    #Plot the original and filtered signal (uncorrupted) in different plots for graphical comparison
    # of the two methods of filtering (lazy approach branch and High res). 
    for i,j,t,f,c in zip(CHUNKED_DATA, Filt, raw_titles, filt_titles, colors_filt):
        plot_sep_sig(chunked_time, i, TIME_NO_SHIFT, j, t, f, c)

    #List the titles to be plotted in Power spectrum
    raw_titles_spec = ['Raw signal Power spectrum (Inverter connected and off)','Raw signal Power spectrum (Inverter connected and on)','Raw signal Power spectrum (Inverter connected, on and WS=5m/s)','Raw signal Power spectrum (Inverter disconnected and off)','Raw signal Power spectrum (Inverter disconnected and on)','Raw signal Power Spectrum (Inverter disconnected, on and WS=5m/s)']
    filt_titles_spec = ['Filtered signal Power spectrum (Inverter connected and off)','Filtered signal Power spectrum (Inverter connected and on)','Filtered signal Power Spectrum (Inverter connected, on and WS=5m/s)','Filtered signal Power Spectrum (Inverter disconnected and off)','Filtered signal Power Spectrum (Inverter disconnected and on)','Filtered signal Power Spectrum (Inverter disconnected, on and WS=5m/s)']
    
    #Plot the raw and filtered signals power spectrums with titles 
    for i,j,t3,t4 in zip(CHUNKED_DATA, Filt, raw_titles_spec, filt_titles_spec):
        f_r, Prr_spec = spect(i)
        plot_spectrum(f_r, Prr_spec,t3)
        f_f, Pff_spec = spect(j)
        plot_spectrum(f_f, Pff_spec, t4)
    
    #List the titles for the Frequency domain plots of the corrupted and uncorrupted samples
    blank_freq_dom_titles = ['Blank filter output with Inverter connected, off','Blank filter output with Inverter connected, on','Blank filter output with Inverter connected, on and WS=5[m/s]','Blank filter output with Inverter disconnected, off','Blank filter output with Inverter disconnected, on','Blank filter output with Inverter disconnected, on and WS=5[m/s]']
    shifted_freq_dom_titles = ['Not shifted filter output with Inverter connected, off','Not shifted filter output with Inverter connected, on', 'Not shifted filter output with Inverter connected, on and WS=5[m/s]','Not shifted filter output with Inverter disconnected, off','Not shifted filter output with Inverter disconnected, on','Not shifted filter output with Inverter disconnected, on and WS=5[m/s]']
    
    #Compute the FFT of raw, corrupted and uncorrupted signals and plot them combined in pairs for comparison 
    for i,j,k,t1,t2 in zip(CHUNKED_DATA,Blank,Filt,blank_freq_dom_titles,shifted_freq_dom_titles):
        f,yin,yout= fft_sig(i,j)
        plot_FFT(f,yin,yout,t1)

        f_sh,yin_sh,yout_sh =fft_sig(i,k)
        plot_FFT(f_sh,yin_sh,yout_sh,t2)


# %%
