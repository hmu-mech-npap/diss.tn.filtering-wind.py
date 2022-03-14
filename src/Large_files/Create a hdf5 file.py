#%%
#Create a hdf5 file and store it in specific location
from venv import create
import numpy as np
import h5py

matrix1= np.random.random(size= (5000,5000))
matrix2= np.random.random(size= (5000,5000))

with h5py.File ('location of the file', 'w') as hdf:
    hdf.create_dataset('dataset1', data=matrix1)
    hdf.create_dataset('dataset2', data=matrix2)


# %%
# read the file that was just created

import numpy as np 
import h5py

with h5py.File('location of the file', 'r') as hdf:
    ls = list(hdf.keys())  
    print ('List of datasets in this file: \n', ls)
    data= hdf.get('dataset1')
    dataset1=np.array(data)
    print('Shape of dataset1: \n', dataset1.shape)
    data2= hdf.get('dataset2')
    dataset2 = np.array(data2)
    print('Shape of dataset2: \n', dataset2.shape)

print(dataset1)
print (dataset2)


# %%
