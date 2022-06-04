# 1.3. Contents of FIR_LP_filter folder

This folder contains 5 files for processing the signal, plotting the raw and filtered signal and generate a dataframe in .h5 file format with the results.

## **functions.py**:
In this file we define all the needed functions for plotting the signal in time and frequency domain as well as to estimate the power spectrum of the signal and computing the Fast Fourier Transform for two separate signals.
- **plot_response ( ) :** 
  - Plots the gain frequency response of the filter based on the coefficients from *signal.freqz()*.
- **spect ( ) :** 
  - Estimates the power spectrum of a given signal via *Welch's method*.
- **plot_spectrum ( ) :**
  - Plots the power spectrum of a given signal using the *spect ( )* function for the needed arguments of (x, y).
- **Axis_titles:**
  - A constructor used to pass axis titles in all functions used for plotting.
- **Time_domain_data_cont:**
  - A class for importing signals in time domain with x,y variables and a label for the legend of the  figure.
- **Signals_for_fft_plot:**
  - Here a constuctor is used to store the output from *fft_sig()* function for the raw and filtered signals and importing x,y components to *plot_FFT*
- **fft_calc_sig:**
  - Here a constructor is used to provide 2 signals for computing the FFT.
- **Fft_Plot_info:**
  - This class is used to store information about the type of the filter used and the output signal state(corrupted from the process or not) as well as the titles of the plots. This is because the *plot_FFT ()* function is constructed in such a way and it is not possible to handle the labels of each signal.
  
- **plot_signals ( ) :**
  - Plots the raw and filtered signal in one figure for better understanding the results of the process. Was modified to work with class objects as input for more information condensation.
  
- **plot_sep_sig ( ) :**
  - Plots the signals in different figures for more information of the Amplitute change from the overall process
- **fft_sig ( ) :**
  - Computes the fft for two given signals with fixed sampling frequency for both. The reason is to compare the filter output before and after the warmup method . *(see: 1.3.3.)*
- **plot_FFT ( ) :**
  - Plots the blank and processed filtered signal's amplitude in frequency domain using the results from *fft_sig ( )* function. 

## **file_import_.py :**
Here a simple function for reading an HDF5 using pandas library is constructed. From this file we can export the raw data in a list form and the keys used in the imported file.
- **data_import ( ) :**
  - Use of **pandas.HDFStore** module for reading the dataframe file.
  - Export the dataframe's contents in a list of *np.ndarrays* and the keys in a separate list of *str*

## **lp_firwin_method_.py**:
In this file we define two functions.
- **lp_firwin ( ) :**
  - Constructs a lowpass FIR analog filter.
- **filt_sig ( ) :**
  -  Uses the above filter and generates a list of ndArrays with
  the filtered signal. 
- **The warmup method :**  
  - Is used to eliminate the time delay of the filter. The time delay of an FIR filter is (N-1)/2, with N= filter order.

##  **plots_time_freq_domain_.py :**
This file is used for plotting the signal in time and frequency domain. It also plots the raw and filtered signals combined. Power spectrum of the original and filtered signal are also produced. Here the old measurements from 08/21 are used.

- *Time domain* :
  - Plots of the raw and filtered signals in combined figures are provided. Here the wind speed and the inverter state are the same in both signals.
- *Spectral dencity* :
  - Here the signals are compared in the same manner as in *time domain* opetation in respect to wind speed and inverter state.
- *frequency domain* :
  - Here each plot presents the raw and filtered signals in the frequency domain. This needs a bit more work as we mention in functions.py file.

## 1.3.5 **create_dataset_.py**
This file is creating an **HDF5** file with the filtered signal and the time interval of the signal without the filter's time delay. 
- File creation:
  
  - Rename the keys of the raw signal dataframe from *xxxxx-raw* to *xxxxx-filt*.
    - **string.replace (old, new, count)** function:
      Allows the replacement of a part of a string without using the **''.join ( )** method.
      ([reference](https://www.geeksforgeeks.org/python-string-replace/))
  
  - A dictionary is constructed with keys the renamed from the raw signal.
    - **dict ( )** function: Creates an empty dictionary 
    - **zip ( )** function: Handles the index for each list and maps them in key:value pairs.

  - Use of **pandas.DataFrame**, **pandas.HDFStore**:
    - Modules for the construction of the dataframe and the creation of the new file in the same folder with the "*...raw.h5* "
  
  - **Optional feature**: 
    - Ask from the user if he wants to change the name of the new file or just replace the *raw* at the end of the file name that was imported to *filt*. 
  
## 1.3.6 **raw_signal_comp.py**
This file is used for .................................
- what it does
  - operation1
  - operation2
  - ....
  -  