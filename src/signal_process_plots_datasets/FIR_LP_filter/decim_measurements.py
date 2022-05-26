#%%

from pathlib import Path
from functions import spect, plot_spect_comb, plot_spectrum
from nptdms import TdmsFile

#%%
#%%


# I use the current working directory of the file to store the folder with the data for ease (FIR_LP_filter/).
folder_path_for_data_now = Path.cwd()

# If you prefear another folder for storing the data use this
# the last line will join the names like a path from the system
#  
# home_folder = Path.home()
# dir_no_1 = 'folder name as a string'
# dir_no_2 = '.....'
# dir_no_3 = '.....' 
# dir_no_4 = '.....'
#
#folder_path_for_data_now = home_folder / dir_no_1 / dir_no_2 / dir_no_3 / dir_no_4 / ..... / .....

#%%

#Constant directories and names for the .tdms file structure
tdms_f_name = 'Data.tdms'
tdms_folder_id = 'WTmeas20220512-'
data_folder_name = 'measurments_12_05_22'

#%% [markdown]
### Inverter measurments comparison with decimated 
## Inverter measurment with :
#   - Inverter On
#   - Wind tunnel speed 0 m/s
#       - first plot at 100 kHz
#       - second plot at 50 kHz
#       - third plot at 5 kHz 
#   

#%%
# Inverter measurments 
# Dir name 
inv_meas_dir = 'Inverter'

WT_inv_1_WS_0 = '115754'

path_inv_meas = folder_path_for_data_now / data_folder_name / inv_meas_dir / f'{tdms_folder_id}{WT_inv_1_WS_0}' / tdms_f_name

tdms_raw_WT =TdmsFile(path_inv_meas)

# Decimation folder measurments 
dec_meas_dir = 'Decimation'
dec_at_50_kHz = '121419'
dec_at_5_kHz = '121435'
path_dec_meas_50_kHz = folder_path_for_data_now / data_folder_name / dec_meas_dir / f'{tdms_folder_id}{dec_at_50_kHz}' / tdms_f_name

path_dec_meas_5_kHz = folder_path_for_data_now / data_folder_name / dec_meas_dir / f'{tdms_folder_id}{dec_at_5_kHz}' / tdms_f_name

tdms_raw_WT_50kHz =TdmsFile(path_dec_meas_50_kHz)
tdms_raw_WT_5kHz =TdmsFile(path_dec_meas_5_kHz)

df_tdms_inv_meas_1_0 = tdms_raw_WT.as_dataframe()

f_spect_WT, Px_x_WT = spect(df_tdms_inv_meas_1_0.iloc[:, 3].values,100_000)

plot_spectrum(f_spect_WT, Px_x_WT, 'Power spectrum of Inverter on and WT:0 [m/s] 100kHz')

#Decimation from original measurment at 50 kHz 
f_spect_WT_dec_50kHz, Px_x_WT_dec_50kHz = spect(df_tdms_inv_meas_1_0.iloc[::2, 3].values, 50_000)

#Decimation from original measurment at 5 kHz
f_spect_WT_dec_5kHz, Px_x_WT_dec_5kHz = spect(df_tdms_inv_meas_1_0.iloc[::20, 3].values,5_000)

df_tdms_dec_50kHz = tdms_raw_WT_50kHz.as_dataframe()
df_tdms_dec_5kHz = tdms_raw_WT_5kHz.as_dataframe()

# Power spectrum frequencies and amplitutes 
f_dec_50kHz, Px_x_dec_50kHz= spect(df_tdms_dec_50kHz.iloc[:, 3], 50_000)
f_dec_5kHz, Px_x_dec_5kHz= spect(df_tdms_dec_5kHz.iloc[:, 3], 5_000)

#Power spectrum at 50kHz
plot_spect_comb(f_spect_WT_dec_50kHz, Px_x_WT_dec_50kHz, f_dec_50kHz, Px_x_dec_50kHz,0,0,title='Decimation at 50kHz',slabel1='Decimated from 100 kHz',slabel2='Decimated measurment', slabel3='')

#Decimation from 50 kHz to 5 kHz
f_dec_50kHz_at_5kHz, Px_x_dec_50kHz_at_5kHz= spect(df_tdms_dec_50kHz.iloc[::10, 3], 5_000)

#Power spectrum at 5kHz
plot_spect_comb(f_spect_WT_dec_5kHz, Px_x_WT_dec_5kHz, f_dec_5kHz, Px_x_dec_5kHz,f_dec_50kHz_at_5kHz,Px_x_dec_50kHz_at_5kHz, title='Decimation at 5kHz',slabel1='Decimated from 100kHz',slabel2='Decimated measurment',slabel3='Decimated from 50kHz')

# %%