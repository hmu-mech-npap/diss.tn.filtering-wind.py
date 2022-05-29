# %%
# Functions and variables to be imported
 
from lp_firwin_method_ import lp_firwin
from scipy import signal

from raw_signal_comp import (df_tdms_0_0, df_tdms_1_0,
                             df_tdms_0_5, df_tdms_1_5,
                             df_tdms_0_11, df_tdms_1_10,
                             f_spect_tdms_CA, Px_x_tdms_CA,
                             FS_100kHz)

from functions import Graph_data_container, spect, plot_spect_comb2

#Constants
FS = FS_100kHz # Sampling frequency of the signal

#Construct an FIR filter with signal.firwin() function
filter_coeff, w, h = lp_firwin(numtaps_2=20, FS=FS, cutoff_Hz=0.0001)

# Filtering of the signal
fir_lp_filt_0_0 = signal.lfilter(filter_coeff, 1.0, df_tdms_0_0.iloc[:, 1].values)
fir_lp_filt_1_0 = signal.lfilter(filter_coeff, 1.0, df_tdms_1_0.iloc[:, 1].values)
fir_lp_filt_0_5 = signal.lfilter(filter_coeff, 1.0, df_tdms_0_5.iloc[:, 1].values)
fir_lp_filt_1_5 = signal.lfilter(filter_coeff, 1.0, df_tdms_1_5.iloc[:, 1].values)
fir_lp_filt_0_11 = signal.lfilter(filter_coeff, 1.0, df_tdms_0_11.iloc[:, 1].values)
fir_lp_filt_1_10 = signal.lfilter(filter_coeff, 1.0, df_tdms_1_10.iloc[:, 1].values)

# FIR filter delay elimination (reject corrupted signal)
warmup = 20-1 #numtaps-1 = order-1
delay = (warmup/2)/FS

# Comp. air 0 m/s
x_fir_0_0, y_fir_0_0 = spect(fir_lp_filt_0_0[warmup:], FS)
x_fir_1_0, y_fir_1_0 = spect(fir_lp_filt_1_0[warmup:], FS)

# Comp.air 5 m/s
x_fir_0_5, y_fir_0_5 = spect(fir_lp_filt_0_5[warmup:], FS)
x_fir_1_5, y_fir_1_5 = spect(fir_lp_filt_1_5[warmup:], FS)

# Comp.air 11/10 m/s
x_fir_0_11, y_fir_0_11 = spect(fir_lp_filt_0_11[warmup:], FS)
x_fir_1_10, y_fir_1_10 = spect(fir_lp_filt_1_10[warmup:], FS)

# Plot the spectral density of the raw and filtered signal for the same Wind speed 
# in one graph

#Inverter Off

# Compressed air 0 m/s
plot_spect_comb2([Graph_data_container(x_fir_0_0, y_fir_0_0, 
                                        label='Filtered FIR'),
                 Graph_data_container(f_spect_tdms_CA[0], Px_x_tdms_CA[0],
                                        label='Raw signal')  ],
                title='Wind speed CA=0 m/s Inverter Off',
                xlim=[1e1,1e5],
                Kolmogorov_offset=1e2,
                figsize = (10,6))


# Compressed air 5 m/s
plot_spect_comb2([Graph_data_container(x_fir_0_5, y_fir_0_5,
                                        label='Filtered'),
                 Graph_data_container(f_spect_tdms_CA[2],Px_x_tdms_CA[2],
                                        label='CA = 5m/s')    ],
                title='Wind speed CA=5 m/s Inverter Off',
                xlim=[1e1,1e5],
                Kolmogorov_offset=1e2,
                figsize=(10,6))

# Compressed air 11 m/s
plot_spect_comb2([Graph_data_container(x_fir_0_11,y_fir_0_11,
                                        label='Filtered FIR'),
                 Graph_data_container(f_spect_tdms_CA[4], Px_x_tdms_CA[4],
                                        label='Raw signal')  ],
                title='Wind speed CA=11 m/s Inverter Off',
                xlim=[1e1,1e5],
                Kolmogorov_offset=1e2,
                figsize = (10,6))

# Inverter On
# Compressed air 0 m/s
plot_spect_comb2([Graph_data_container(x_fir_1_0, y_fir_1_0,
                                        label='Filtered FIR'),
                 Graph_data_container(f_spect_tdms_CA[1], Px_x_tdms_CA[1],
                                        label='Raw signal')  ],
                title='Wind speed CA=0 m/s Inverter On',
                xlim=[1e1,1e5],
                Kolmogorov_offset=1e2,
                figsize=(10,6))

# Compressed air 5 m/s
plot_spect_comb2([Graph_data_container(x_fir_1_5,y_fir_1_5,
                                        label='Filtered FIR'),
                 Graph_data_container(f_spect_tdms_CA[3], Px_x_tdms_CA[3],
                                        label='Raw signal')  ],
                title='Wind speed CA=5 m/s Inverter On',
                xlim=[1e1,1e5],
                Kolmogorov_offset=1e2,
                figsize=(10,6))

# Compressed air 10 m/s
plot_spect_comb2([Graph_data_container(x_fir_1_10, y_fir_1_10,
                                        label='Filtered FIR'),
                 Graph_data_container(f_spect_tdms_CA[5], Px_x_tdms_CA[5],
                                        label='Raw signal')  ],
                title='Wind speed CA=11 m/s Inverter On',
                xlim=[1e1,1e5],
                Kolmogorov_offset=1e2,
                figsize = (10,6))


# %%
