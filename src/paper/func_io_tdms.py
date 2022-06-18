#%%
from pathlib import Path

from nptdms import TdmsFile


def compressed_air_data(folder_for_data:Path)-> dict: 
    """returns a dictionary with :
      - keys : the short IDs fo the compressed air data
      - values : the tdmps files 

    Args:
        FOLDER_FOR_DATA (Path): _description_

    Returns:
        dict: _description_
    """    
    #Constant directories and names for the .tdms file structure
    comp_air_dir = folder_for_data/ 'compressed air'
    TDMS_FNAME = 'Data.tdms'

    # Dir names for the Compressed air measurment

    data_CA_inv_0_WS_0 = 'ca0_0.1'
    data_CA_inv_0_WS_5 = 'ca0_5.1'
    data_CA_inv_0_WS_11= 'ca0_10.1'
    data_CA_inv_1_WS_0 = 'ca1_0.1' 
    data_CA_inv_1_WS_5 = 'ca1_5.1'
    data_CA_inv_1_WS_10= 'ca1_10.1'

    path_comp = folder_for_data / comp_air_dir

    # CA stands for compressed air

    raw_signal_CA = [data_CA_inv_0_WS_0, data_CA_inv_0_WS_5, 
                    data_CA_inv_0_WS_11, data_CA_inv_1_WS_0,
                    data_CA_inv_1_WS_5, data_CA_inv_1_WS_10 ]

    tdms_raw_CA = []

    for item in raw_signal_CA:
        y = f'{path_comp}/{item}'
        x=TdmsFile( Path( y , TDMS_FNAME))
        tdms_raw_CA.append(x)
    
    return {k:v for k,v in zip(raw_signal_CA, tdms_raw_CA)}


def inverter_data(folder_for_data:Path)-> dict: 
    """returns a dictionary with :
      - keys : the short IDs fo the Inverter data
      - values : the tdmps files 

    Args:
        FOLDER_FOR_DATA (Path): _description_

    Returns:
        dict: _description_
    """    
    #Constant directories and names for the .tdms file structure
    comp_air_dir = folder_for_data/ 'Inverter'
    TDMS_FNAME = 'Data.tdms'

    # Dir names for the Compressed air measurment

    data__inv_0_WS_0  = 'in0_0.1'
    data__inv_1_WS_0  = 'in1_0.1'
    data__inv_1_WS_5  = 'in1_5.1'
    data__inv_1_WS_10 = 'in1_10.1' 
    data__inv_1_WS_15 = 'in1_15.1'
    data__inv_1_WS_20 = 'in1_20.1'

    path_comp = folder_for_data / comp_air_dir

    # CA stands for compressed air

    raw_signal_inv = [data__inv_0_WS_0, 
                    data__inv_1_WS_0, 
                    data__inv_1_WS_5, 
                    data__inv_1_WS_10,
                    data__inv_1_WS_15, 
                    data__inv_1_WS_20 ]

    tdms_raw_inv = []

    for item in raw_signal_inv:
        y = f'{path_comp}/{item}'
        x=TdmsFile( Path( y , TDMS_FNAME))
        tdms_raw_inv.append(x)
    
    return {k:v for k,v in zip(raw_signal_inv, tdms_raw_inv)}

def decimation_data(folder_for_data:Path)-> dict: 
    """returns a dictionary with :
      - keys : the short IDs fo the Inverter data
      - values : the tdmps files 

    Args:
        FOLDER_FOR_DATA (Path): _description_

    Returns:
        dict: _description_
    """    
    #Constant directories and names for the .tdms file structure
    comp_air_dir = folder_for_data/ 'Decimation'
    TDMS_FNAME = 'Data.tdms'

    # Dir names for the Compressed air measurment

    data_50kHz_ws0  = 'de50.1'
    data_5kHz_ws0  = 'de5.1'

    path_comp = folder_for_data / comp_air_dir

    # CA stands for compressed air

    raw_signal_de = [data_50kHz_ws0, 
                    data_5kHz_ws0 ]

    tdms_raw_de = []

    for item in raw_signal_de:
        y = f'{path_comp}/{item}'
        x=TdmsFile( Path( y , TDMS_FNAME))
        tdms_raw_de.append(x)
    
    return {k:v for k,v in zip(raw_signal_de, tdms_raw_de)}


def all_data(folder_for_data:Path)-> dict: 
    """wrapper function to retun a dictionariy with all the objects.

    Args:
        folder_for_data (Path): _description_

    Returns:
        dict: _description_
    """    
    
    d_ca= compressed_air_data(folder_for_data=folder_for_data)
    d_in= inverter_data(folder_for_data=folder_for_data)
    d_de= decimation_data(folder_for_data=folder_for_data)
    try:
        d_all = (d_ca |d_in) | d_de # only works on python 3.9
    except:
        d_all = dict(**d_ca, **d_in, **d_de) # fallback method, works on every version
    return d_all
# %%
if __name__=='__main__':


    FOLDER_FOR_DATA = Path('/mnt/data_folder/measurements_12_05_22/new_record_prop_channel/')
    if not FOLDER_FOR_DATA.exists():   
        FOLDER_FOR_DATA = Path('D:/_data/WEL/WEL20220512/')

    d_ca= compressed_air_data(folder_for_data=FOLDER_FOR_DATA)
    d_in= inverter_data(folder_for_data=FOLDER_FOR_DATA)
    d_de= decimation_data(folder_for_data=FOLDER_FOR_DATA)
    d_all = (d_ca |d_in) | d_de

# %%
