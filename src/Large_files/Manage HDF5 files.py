#%%
#Use of h5py library for reading the keys of hdf5 file format
import h5py
f = h5py.File('/home/goodvibrationskde/Documents/hdf5_sample_data.h5', 'r')

# find out how many sets of data are in the file
f.keys()
print(f.keys())

#find out how the file was created (here <class 'h5py._hl.dataset.Dataset>')
dataset1= f.get('dataset1')
print(type(dataset1))
f.close()


# %%
#Use of pandas library for reading hdf5 file format

import numpy as np
import pandas as pd


f_1 = pd.HDFStore(path='/home/goodvibrationskde/Documents/hdf5_sample_data.h5', mode='r')
f_1.keys()
print(f_1.keys())
f_1.close()

# %%
