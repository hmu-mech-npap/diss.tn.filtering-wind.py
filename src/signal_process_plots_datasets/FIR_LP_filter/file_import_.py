import numpy as np 
import pandas as pd

def data_import(file_path:str, file_name_of_raw:str):
    """file import script and data chunking for faster overall process time

    Args:
        file_path (str): the file path of the folder containing the HDF5 file
        file_name_of_raw (str): the name of the file to import
    Returns:
        MATRIX_RAW (list): a list of np.ndarrays transformed columns from dataset
        L (list): a list of the dataframes keys in str format
        List_of_chunked (list): Here we store the sampled raw
        signal from the dataset with a constant rate 

    """

    # #Read and store the .h5 file with pandas
    # f_1 = pd.HDFStore(path='/home/goodvibrations32/Documents/Git_clones_dissertation/DSP_Filters_Python-/src/data_folder/noise_reference_raw.h5', mode='r')
    # 
    # #Store all the dataframe in a variable
    # data_raw = f_1['/df']
    # 

    #file_path = input('The full path of raw data file to process: ' )
    #file_name_of_raw =input('Enter the name of the raw signal file :') 

    #Read and store the .h5 file with pandas
    f_1 = pd.HDFStore(path=f'{file_path}{file_name_of_raw}', mode='r')

    print('The data frame key is: ',f_1.keys())


    data_raw = f_1['df']

    #Chunking of data with a constant sample rate
    rate_of_sampling = 10

    chunked_data = data_raw[::rate_of_sampling]
    List_of_chunked = []

    #Make a list with present keys
    L = list(data_raw.keys())

    #Store the chunked data in a list for the signal processing operations
    for element1 in L:
        List_of_chunked.append(np.array(chunked_data.get(element1)))
    print(data_raw.info())

    #Manage data with lists 
    MATRIX_RAW = []
    for element0 in L:
        MATRIX_RAW.append(np.array(data_raw.get(element0)))
    
    return MATRIX_RAW, L, List_of_chunked