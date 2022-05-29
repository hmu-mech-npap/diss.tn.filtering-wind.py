# %%

from pathlib import Path
from matplotlib import pyplot as plt
from nptdms import TdmsFile
import numpy as np

from functions import spect, plot_spect_comb, plot_spectrum, plot_spect_comb2, Graph_data_container


# %% [markdown]
# ## Here the new measurments from 12/05/22 are used
# # Plots of power spectrums respectivly
#  ### The first 3 plots are a comparison between the signals with the compressed air.
#  - Here the signals are compared with respect of the Inverter state
#       - **on/off**

# %%
#CONSTANTS

# I use the current working directory of the file to store the folder with the data for ease (FIR_LP_filter/).
#FOLDER_FOR_DATA = Path.cwd()/'measurements_12_05_22'
FOLDER_FOR_DATA = Path('D:/_data/WEL/WEL20220512/')

# If you prefear another folder for storing the data use this
# the last line will join the names like a path from the system
#  
# home_folder = Path.home()
# dir_no_1 = 'folder name as a string'
# dir_no_2 = '.....'
# dir_no_3 = '.....' 
# dir_no_4 = '.....'
#
#FOLDER_FOR_DATA = home_folder / dir_no_1 / dir_no_2 / dir_no_3 / dir_no_4 / ..... / .....


#Constant directories and names for the .tdms file structure
tdms_folder_id = 'WTmeas20220512-'
tdms_f_name = 'Data.tdms'

# Dir names for the Compressed air measurment
comp_air_dir = 'compressed air'

data_CA_inv_0_WS_0 = '112318'
data_CA_inv_0_WS_5 = '112629'
data_CA_inv_0_WS_11= '112709'
data_CA_inv_1_WS_0 = '113005' 
data_CA_inv_1_WS_5 = '113534'
data_CA_inv_1_WS_10= '113614'

path_comp = FOLDER_FOR_DATA / comp_air_dir / tdms_folder_id

# CA stands for compressed air

raw_signal_CA = [data_CA_inv_0_WS_0, data_CA_inv_0_WS_5, 
                data_CA_inv_0_WS_11, data_CA_inv_1_WS_0,
                data_CA_inv_1_WS_5, data_CA_inv_1_WS_10 ]

tdms_raw_CA = []

for item in raw_signal_CA:
    y = f'{path_comp}{item}'
    x=TdmsFile( Path( y , tdms_f_name))
    tdms_raw_CA.append(x)


df_tdms_0_0 = tdms_raw_CA[0].as_dataframe()
df_tdms_0_5 = tdms_raw_CA[1].as_dataframe()
df_tdms_0_11 = tdms_raw_CA[2].as_dataframe()
df_tdms_1_0 = tdms_raw_CA[3].as_dataframe()
df_tdms_1_5 = tdms_raw_CA[4].as_dataframe()
df_tdms_1_10 = tdms_raw_CA[5].as_dataframe()
f_spect_tdms_CA=[]
Px_x_tdms_CA=[]

# Estimate the power spectral density of the raw signal
# Hotwire speed 0 m/s
x2,y2 = spect(df_tdms_1_0.iloc[:, 1].values, FS=100_000)
x,y = spect(df_tdms_0_0.iloc[:, 1].values, FS=100_000)

# Hotwire speed 5 m/s
x_2,y_2 = spect(df_tdms_1_5.iloc[:, 1].values,100_000)
x_,y_ = spect(df_tdms_0_5.iloc[:, 1].values, 100_000)    
# Hotwire speed 10/11 m/s
x_3,y_3 = spect(df_tdms_1_10.iloc[:, 1].values,100_000)
x__,y__ = spect(df_tdms_0_11.iloc[:, 1].values,100_000)

# Append those values in lists for later usage with indexes (for loops opt.)
# Hotwire speed 0 m/s
f_spect_tdms_CA.append(x)
f_spect_tdms_CA.append(x2)
Px_x_tdms_CA.append(y)
Px_x_tdms_CA.append(y2)

# Hotwire speed 5 m/s


plot_spect_comb2([Graph_data_container(f_spect_tdms_CA[0], Px_x_tdms_CA[0],  label= 'Inverter:Off'),
                 Graph_data_container( f_spect_tdms_CA[1], Px_x_tdms_CA[1], label= 'Inverter:On')   ],
                title='Wind speed CA=0 m/s',
                xlim =[1e1,1e5],
                Kolmogorov_offset=1e2)

#%% [markdown]
## Same for 5 m/s WS Comp. Air
#%%
x_2,y_2 = spect(df_tdms_1_5.iloc[:, 1].values,100_000)
x_,y_ = spect(df_tdms_0_5.iloc[:, 1].values, 100_000)
f_spect_tdms_CA.append(x_)
f_spect_tdms_CA.append(x_2)
Px_x_tdms_CA.append(y_)
Px_x_tdms_CA.append(y_2)

# Hotwire speed 10/11 m/s


plot_spect_comb2([Graph_data_container(f_spect_tdms_CA[2], Px_x_tdms_CA[2], 
                                       label= 'Inverter:Off'),
                 Graph_data_container( f_spect_tdms_CA[3], Px_x_tdms_CA[3],
                                      label= 'Inverter:On')   ],
                title='Wind speed CA=5 m/s',
                xlim =[1e1,1e5],
                Kolmogorov_offset=1e2, figsize = (10,6))
#%% [markdown]
## Same for 10/11 WS Comp. Air
#%%
x_3,y_3 = spect(df_tdms_1_10.iloc[:, 1].values,100_000)
x__,y__ = spect(df_tdms_0_11.iloc[:, 1].values,100_000)
f_spect_tdms_CA.append(x__)
f_spect_tdms_CA.append(x_3)
Px_x_tdms_CA.append(y__)
Px_x_tdms_CA.append(y_3)


# %%
plot_spect_comb2([Graph_data_container( f_spect_tdms_CA[4], Px_x_tdms_CA[4], label= 'Inverter:Off, WS:10 m/s'),
                 Graph_data_container( f_spect_tdms_CA[5], Px_x_tdms_CA[5], label= 'Inverter:On, WS:11 m/s')   ],
                title='Wind speed CA=10/11 m/s',
                xlim =[1e1,1e5],
                Kolmogorov_offset=1e2, to_disk=True)


def main():

    plot_spect_comb(f_spect_tdms_CA[0], Px_x_tdms_CA[0],
                    f_spect_tdms_CA[1], Px_x_tdms_CA[1],
                    0,0,
                    title='Wind speed CA=0 m/s',
                    slabel1='Inverter:Off',
                    slabel2='Inverter:On',slabel3='',
                    xlim=[1e1,1e5])


    plot_spect_comb(f_spect_tdms_CA[2], Px_x_tdms_CA[2], 
                    f_spect_tdms_CA[3], Px_x_tdms_CA[3],
                    0,0,
                    title='Wind speed CA=5 m/s',
                    slabel1='Inverter:Off',
                    slabel2='Inverter:On',slabel3='',
                    xlim=[1e1,1e5])

    plot_spect_comb(f_spect_tdms_CA[4], Px_x_tdms_CA[4], 
                    f_spect_tdms_CA[5], Px_x_tdms_CA[5],
                    0,0,
                    title='Wind speed CA=10/11 m/s',
                    slabel1='Inverter:Off, WS:10 m/s',
                    slabel2='Inverter:On, WS:11 m/s', slabel3='',
                    xlim =[1e1,1e5])


# Construct the desiered FIR filter


if __name__ == "__main__":
    main()

# %%
# %%
