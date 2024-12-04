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

import ae_process_algos as aepe
from pathlib import Path
from os import listdir
import pandas as pd
import numpy as np
import ast

#########################################
# User inputs
#########################################

Folder_With_Data = "data_out"

No_Defect_Files = [
                "Defect_Web_1st_Place_Resonance_150_100_Iters_11-0-47",
                "Defect_Web_2nd_Place_Resonance_150_100_Iters_11-6-8",
                "Defect_Web_3rd_Place_Resonance_150_100_Iters_11-10-43",
                "Defect_Head_1st_Place_Resonance_150_100_Iters_10-38-56",
                "Defect_Head_2nd_Place_Resonance_150_100_Iters_10-46-0",
                "Defect_Head_3rd_Place_Resonance_150_100_Iters_10-56-16"
                ]

Defect_Files = [
                "No_Defect_Web_1st_Place_Resonance_150_100_Iters_10-41-12",
                "No_Defect_Web_2nd_Place_Resonance_150_100_Iters_10-49-15",
                "No_Defect_Web_3rd_Place_Resonance_150_100_Iters_10-54-35",
                "No_Defect_Head_1st_Place_Resonance_150_100_Iters_10-11-22",
                "No_Defect_Head_2nd_Place_Resonance_150_100_Iters_10-18-9",
                "No_Defect_Head_3rd_Place_Resonance_150_100_Iters_10-26-34"
                ]

sample_rate = ((125E6)/32) # The ammount of samples taken in a secound.

lower_frequency = 120000
higher_frequency = 180000
threshold = 0.2
roll_off = 50

#########################################
# Functions To Run
#########################################

def compute_all_ae_processing_algos(signal,sample_rate,lower_frequency,higher_frequency,threshold,roll_off):
    """
    Computes all the ae processing algos for a specific row.
    Meant to be used with the apply statement in pandas.
    Row format is the one that measure produces in this git page.

    Args:
        x: represents the row in the data frame
        sample_rate: the sample rate when recording the signal
        lower_frequency: the lower frequency that is choosen for band energy calculations
        higher_frequency: the higher frequency that is choosen for band energy calculations
        threshold: the amplitude where it will start counting above that.
        roll_off: percentage for the roll off calculations (0-100)
    
    Returns:
        A list of all the new properties to add to the row.

    """

    # Set up to run functions one after another.
    spectrum = aepe.singal_to_Spectrum(signal)

    return pd.Series({
            "band_energy": aepe.band_energy(spectrum,sample_rate,lower_frequency,higher_frequency),
            "band_energy_ratio": aepe.band_energy_ratio(spectrum,sample_rate,lower_frequency,higher_frequency),
            "clearance_factor": aepe.clearance_factor(signal),
            "counts": aepe.counts(signal,threshold),
            "crest_factor": aepe.crest_factor(signal),
            "energy": aepe.energy(signal),
            "impulse_factor": aepe.impulse_factor(signal),
            "k_factor": aepe.k_factor(signal),
            "kurtosis": aepe.kurtosis(signal),
            "margin_factor": aepe.margin_factor(signal),
            "peak_amplitude": aepe.peak_amplitude(signal),
            "rms": aepe.rms(signal),
            "shape_factor": aepe.shape_factor(signal),
            "skewness": aepe.skewness(signal),
            "spectral_centroid": aepe.spectral_centroid(spectrum,sample_rate),
            "spectral_kurtosis": aepe.spectral_kurtosis(spectrum,sample_rate),
            "spectral_peak_frequency": aepe.spectral_peak_frequency(spectrum,sample_rate),
            "spectral_rolloff": aepe.spectral_rolloff(spectrum,sample_rate,roll_off),
            "spectral_skewness": aepe.spectral_skewness(spectrum,sample_rate),
            "spectral_variance": aepe.spectral_variance(spectrum,sample_rate),
            "zero_crossing_rate": aepe.zero_crossing_rate(signal,sample_rate)
            })


    #TODO: Create this function to use apply on data frame to make code nicer for computing all properties.




#########################################
# Main Function running.
#########################################

# First perform all the processing on each file in turn
Files_In_Folder = listdir(Folder_With_Data)
for File in Files_In_Folder:
    #TODO: Create some way to store the processed data frame. and retrieve it afterwards when comparing between files.
    filepath = Path(Folder_With_Data + "/" + File)

    # Importing dataframe and create data frame to file in
    # Importing dataframe and adding the new rows which will be solved for.
    Data_Frame = pd.read_csv(filepath)

    # Converting signal column 
    Data_Frame['Signal'] = Data_Frame['Signal'].apply(
            lambda x: list(map(float, ast.literal_eval(x))) if pd.notnull(x) else [])
    Data_Frame['Signal'] = Data_Frame['Signal'].apply(np.array)

    # Using the apply statement to calculate all ae properties for each data frame row
    # Then adding it to the relevent columns for later processing.
    Data_Frame[[
        "band_energy",
        "band_energy_ratio",
        "clearance_factor",
        "counts",
        "crest_factor",
        "energy",
        "impulse_factor",
        "k_factor",
        "kurtosis",
        "margin_factor",
        "peak_amplitude",
        "rms",
        "shape_factor",
        "skewness",
        "spectral_centroid",
        "spectral_kurtosis",
        "spectral_peak_frequency",
        "spectral_rolloff",
        "spectral_skewness",
        "spectral_variance",
        "zero_crossing_rate"
        ]] = Data_Frame.apply(
            lambda row: compute_all_ae_processing_algos(
                row["Signal"],
                sample_rate,
                lower_frequency,
                higher_frequency,
                threshold,
                roll_off
                ),axis=1)

    print(Data_Frame)
    print("Wait")

    #TODO: Create a function to make a string to run all of the relevent functions that a user defines in a list. Make it create the new columns in the data frame and run the funtions of the values.
    #TODO: create a function to execute the ae processing algos that we specify in a list. Make it a function.


    #TODO: Calculate the binomial probabilities for each property accross each file. Mean and standard deviation.