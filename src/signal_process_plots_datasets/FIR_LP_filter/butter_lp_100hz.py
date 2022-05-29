# %%
# Libraries, functions and variables to be imported

import numpy as np
from scipy import signal

from raw_signal_comp import (df_tdms_0_0, df_tdms_1_0,
                            df_tdms_0_5, df_tdms_1_5,
                            df_tdms_0_11, df_tdms_1_10,
                            f_spect_tdms_CA, Px_x_tdms_CA,
                            FS_100kHz)

from functions import spect, plot_spect_comb2, Graph_data_container

# Constants
FS = FS_100kHz

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
plot_spect_comb2([Graph_data_container(x_filt,y_filt,
                                        label='Filtered Butterworth'),
                 Graph_data_container(f_spect_tdms_CA[0],Px_x_tdms_CA[0],
                                        label='Raw signal')    ],
                title='Wind speed CA=0 m/s Inverter Off',
                xlim=[1e1,1e5],
                Kolmogorov_offset=1e2,
                figsize=(10,6),
                #to_disk=True
                )

# Same for 5 m/s WS Comp. Air
plot_spect_comb2([Graph_data_container(x_filt_ws_5,y_filt_ws_5,
                                        label='Filtered Butterworth'),
                 Graph_data_container(f_spect_tdms_CA[2],Px_x_tdms_CA[2],
                                        label='Raw signal')    ],
                title='Wind speed CA=5 m/s Inverter Off',
                xlim=[1e1,1e5],
                Kolmogorov_offset=1e2,
                figsize=(10,6),
                #to_disk=True
                )

# Same for 11 m/s WS Comp. Air
plot_spect_comb2([Graph_data_container(x_filt_ws_11,y_filt_ws_11,
                                        label='Filtered Butterworth'),
                 Graph_data_container(f_spect_tdms_CA[4],Px_x_tdms_CA[4],
                                        label='Raw signal')    ],
                title='Wind speed CA=11 m/s Inverter Off',
                xlim=[1e1,1e5],
                Kolmogorov_offset=1e2,
                figsize=(10,6),
                #to_disk=True
                )

# Inverter on
# Compare the signals for 0 m/s WS Comp.Air
plot_spect_comb2([Graph_data_container(x2_filt,y2_filt,
                                        label='Filtered Butterworth'),
                 Graph_data_container(f_spect_tdms_CA[1],Px_x_tdms_CA[1],
                                        label = 'Raw signal')  ],
                title='Wind speed CA=0 m/s Inverter On',
                xlim=[1e1,1e5],
                Kolmogorov_offset=1e2,
                figsize=(10,6),
                #to_disk=True
                )

# Same for 5 m/s WS Comp. Air
plot_spect_comb2([Graph_data_container(x2_filt_ws_5,y2_filt_ws_5,
                                        label='Filtered Butterworth'),
                 Graph_data_container(f_spect_tdms_CA[3], Px_x_tdms_CA[3],
                                        label='Raw signal')   ],
                title='Wind speed CA=5 m/s Inverter On',
                xlim=[1e1,1e5],
                Kolmogorov_offset=1e2,
                figsize=(10,6),
                #to_disk=True
                )

# Same for 10 m/s WS Comp. Air
plot_spect_comb2([Graph_data_container(x2_filt_ws_10,y2_filt_ws_10,
                                        label='Filtered Butterworth'),
                 Graph_data_container(f_spect_tdms_CA[5],Px_x_tdms_CA[5],
                                        label='Raw signal')    ],
                title='Wind speed CA=11 m/s Inverter On',
                xlim=[1e1,1e5],
                Kolmogorov_offset=1e2,
                figsize=(10,6),
                #to_disk=True
                )


# %%
