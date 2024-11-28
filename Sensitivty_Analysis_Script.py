"""
This script is going to be used to compleate the sensitivity study with the AE Sensors.

It will use all of the AE processing algorithums.
It will output a processed data frame with all those properties
adding those columns to the final dataframe.

Statistical analysis between the mean and standard deviations will be done.
Will compare binomial distrabution curves.

"""

#########################################
# Packages/ other python files to import.
#########################################

import AE_Processing_Algorithms as AEPA
from pathlib import Path
from os import listdir
import pandas as pd

#########################################
# User inputs
#########################################

Folder_With_Data = "data_out"

No_Defect_Files = [
                "Defect_Web_1st_Place_Resonance_150_100_Iters_11-0-47",
                "Defect_Web_2nd_Place_Resonance_150_100_Iters_11-6-8",
                "Defect_Web_3rd_Place_Resonance_150_100_Iters_11-10-43"
                ]

Defect_Files = [
                "No_Defect_Web_1st_Place_Resonance_150_100_Iters_10-41-12",
                "No_Defect_Web_2nd_Place_Resonance_150_100_Iters_10-49-15",
                "No_Defect_Web_3rd_Place_Resonance_150_100_Iters_10-54-35"
                ]


#########################################
# Functions To Run
#########################################

def Compute_All_AE_Processing_Algos(x):

    Signal = # Figure out syntax
    #TODO: Create this function to use apply on data frame to make code nicer for computing all properties.




#########################################
# User inputs
#########################################

# First perform all the processing on each file in turn
Files_In_Folder = listdir(Folder_With_Data)
for File in Files_In_Folder:
    filepath = Path(Folder_With_Data + "/" + File)

    # Importing dataframe and create data frame to file in
    Un_Processed_Data_Frame = pd.read_csv(filepath)

    Processed_Data_Frame = Un_Processed_Data_Frame[[
                                                "band_energy",
                                                "band_energy_ratio",
                                                ]]
    #TODO: create the new data frame by adding the new columns.

    df.apply( ,axis=1, )
    #TODO: create this apply statement and get it all working as expected returning the processed data frame

    #TODO: Create a function to make a string to run all of the relevent functions that a user defines in a list. Make it create the new columns in the data frame and run the funtions of the values.
    