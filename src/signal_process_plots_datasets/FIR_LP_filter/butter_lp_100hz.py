# %%

# ===============================================================================
# I think this file could be replaced and deleted permenantly because the
# class you made is filtering much faster the signal with a butterworth filter
# and is replacing the hole file I think... 
# =============================================================================== 

# Libraries, functions and variables to be imported
import numpy as np
from scipy import signal
from raw_signal_comp import df_tdms_0_0, df_tdms_1_0, df_tdms_0_5, df_tdms_1_5, df_tdms_0_11, df_tdms_1_10, f_spect_tdms_CA, Px_x_tdms_CA
from functions import spect, plot_spect_comb

# Constants
FS = 100_000

# Construction of Butterworth filter
sos = signal.butter(N = 10, Wn = 200*np.pi, btype = 'lp', fs = FS, output = 'sos')

# Filtering the signals of all compressed air measurements
filtered_inv1_ws0 = signal.sosfilt(sos, df_tdms_1_0.iloc[:, 1].values)
filtered_inv0_ws0 = signal.sosfilt(sos, df_tdms_0_0.iloc[:, 1].values)
filtered_inv1_ws5 = signal.sosfilt(sos, df_tdms_1_5.iloc[:, 1].values)
filtered_inv0_ws5 = signal.sosfilt(sos, df_tdms_0_5.iloc[:, 1].values)
filtered_inv1_ws10 = signal.sosfilt(sos, df_tdms_1_10.iloc[:, 1].values)
filtered_inv0_ws11 = signal.sosfilt(sos, df_tdms_0_11.iloc[:, 1].values)

# Estimate spectral density of filtered signal from IIR butterworth filter 
x2_filt,y2_filt = spect(filtered_inv1_ws0, FS=FS)
x_filt,y_filt = spect(filtered_inv0_ws0, FS=FS)

x2_filt_ws_5,y2_filt_ws_5 = spect(filtered_inv1_ws5, FS=FS)
x_filt_ws_5,y_filt_ws_5 = spect(filtered_inv0_ws5, FS=FS)

x2_filt_ws_10,y2_filt_ws_10 = spect(filtered_inv1_ws10, FS=FS)
x_filt_ws_11,y_filt_ws_11 = spect(filtered_inv0_ws11, FS=FS)

# Plot the raw and filtered signal spectral densities in one graph for comparison

# Inverter off
# Compare the signals for 0 m/s WS Comp.Air
plot_spect_comb(x1=x_filt,y1=y_filt,
                x2=f_spect_tdms_CA[0],y2=Px_x_tdms_CA[0],
                x3=0,y3=0,
                title='Wind speed CA=0 m/s Inverter Off',
                slabel1='Filtered Butterworth',
                slabel2='Raw signal',slabel3='',
                xlim=[1e1,1e5]
                )

# Same for 5 m/s WS Comp. Air
plot_spect_comb(x1=x_filt_ws_5,y1=y_filt_ws_5,
                x2=f_spect_tdms_CA[2],y2= Px_x_tdms_CA[2],
                x3=0,y3=0,
                title='Wind speed CA=5 m/s Inverter Off',
                slabel1='Filtered Butterworth',
                slabel2='Raw signal',slabel3='',
                xlim=[1e1,1e5]
                )

# Same for 10/11 m/s WS Comp. Air
plot_spect_comb(x1=x_filt_ws_11,y1=y_filt_ws_11,
                x2=f_spect_tdms_CA[4],y2=Px_x_tdms_CA[4],
                x3=0,y3=0,
                title='Wind speed CA=11 m/s Inverter Off',
                slabel1='Filtered Butterworth',
                slabel2='Raw signal',slabel3='',
                xlim=[1e1,1e5]
                )

# Inverter on
# Compare the signals for 0 m/s WS Comp.Air
plot_spect_comb(x1=x2_filt,y1=y2_filt,
                x2=f_spect_tdms_CA[1],y2=Px_x_tdms_CA[1],
                x3=0,y3=0,
                title='Wind speed CA=0 m/s Inverter On',
                slabel1='Filtered Butterworth',
                slabel2='Raw signal',slabel3='',
                xlim=[1e1,1e5]
                )

# Same for 5 m/s WS Comp. Air
plot_spect_comb(x1=x2_filt_ws_5,y1=y2_filt_ws_5,
                x2=f_spect_tdms_CA[3],y2= Px_x_tdms_CA[3],
                x3=0,y3=0,
                title='Wind speed CA=5 m/s Inverter On',
                slabel1='Filtered Butterworth',
                slabel2='Raw signal',slabel3='',
                xlim=[1e1,1e5]
                )

# Same for 10/11 m/s WS Comp. Air
plot_spect_comb(x1=x2_filt_ws_10,y1=y2_filt_ws_10,
                x2=f_spect_tdms_CA[5],y2=Px_x_tdms_CA[5],
                x3=0,y3=0,
                title='Wind speed CA=11 m/s Inverter On',
                slabel1='Filtered Butterworth',
                slabel2='Raw signal',slabel3='',
                xlim=[1e1,1e5]
                )

# %%
