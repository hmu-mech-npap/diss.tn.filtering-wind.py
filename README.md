![ci tests](https://github.com/goodvibrations32/diss.tn.filtering-wind.py/actions/workflows/actions.yaml/badge.svg)
# diss.tn.filtering-wind.py
This is a dissertation repository for torosian Nikolaos for filtering.

## Naming convention
All words and numbers in filenames should be separated via underscores (word_1.xxx) 
For variables convention: 
  - CA = Compressed Air
  - inv_0 = Inverter off
  - inv_1 = Inverter on
  - WS_0 = Wind Speed is 0 [m/s]
## Data folder path import
The folder path imported for the data files/folders is stored in the variable "FOLDER_FOR_DATA" and the user should change it to match the location of the data folder in their system. After this the folder structure for .tdms datasets should change accordingly. 
## Brief folder description
1. **src/Filtering_A_signal :** In this folder are some example usage for various filters. 
2. **src/data_folder :** Here we store the first dataset recorded in 2021.
3. **src/paper :** This folder created by N.Papadakis is used to produce some user readable plots for writing a paper on the matter.
4. **src/sampleGUI :** This folder is for developing a GUI frontend app for the user.
5. **src/signal_process :** Here the main analysis of the signals implemented with the use of pypkg which one can find in the main project's folder. 
6. **src/understanding :** Here we test all new ideas and implementations of methods and also cross examine different approaches.
