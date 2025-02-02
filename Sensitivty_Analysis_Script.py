"""
This script is going to be used to compleate the sensitivity study with the AE Sensors.

It will use all of the AE processing algorithums.
It will output a processed data frame with all those properties
adding those columns to the final dataframe.

Statistical analysis between the mean and standard deviations will be done.
Will compare normal distrabution curves.

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
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import scipy.stats as stats

#########################################
# User inputs
#########################################

folder_with_data = "data_out"
pdf_output = "pdf_reports" # folder where pdfs will be saved to.
pdf_file_name = "normal_distrabution_plots_head.pdf" # name of pdf file that will be created.

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

def normal_dis_plot(mean,std,line_name):
    """
    Function to take the mean and standard deviation and plot the normal distrabution
    
    Args:
        mean: normal distrabution mean
        std: normal distrabution standard deviation
        line_name: name that line will be given

    Returns:
        plots a line of the normal distrabution

    """
    x_values = np.linspace(mean - 1*std, mean + 1*std, 100)
    #TODO: chnage the 1 to a variable you can adjust at the top. 
    plt.plot(x_values, stats.norm.pdf(x_values, mean, std), label=line_name)


#########################################
# Setup
#########################################

# Files in folder we are working on.
files_in_folder = listdir(folder_with_data)

# List the properties that will be calculated.
properties_to_calculate = [
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
    "zero_crossing_rate"]

# Creating a blank data frame to hold all the processed data means and standard deviations from each file
# Will then be used to compare against each other with line plots and see how it all differs
normal_mean_processed = pd.DataFrame(
    columns=properties_to_calculate, index=files_in_folder)
normal_std_processed = pd.DataFrame(
    columns=properties_to_calculate, index=files_in_folder)


#########################################
# Main Processing of data
#########################################

# process signal data and save mean and standard deviation.
for file in files_in_folder:

    # Importing dataframe
    file_data_frame = pd.read_csv(Path(folder_with_data + "/" + file))

    # Converting signal column to numpy array from string
    file_data_frame['Signal'] = file_data_frame['Signal'].apply(
        lambda x: list(map(float, ast.literal_eval(x))) if pd.notnull(x) else [])
    file_data_frame['Signal'] = file_data_frame['Signal'].apply(np.array)

    # Using the apply statement to calculate all ae properties for each data frame row
    # Then adding a column for that property
    processed_data_frame = file_data_frame.apply(
            lambda row: compute_all_ae_processing_algos(
                row["Signal"],
                sample_rate,
                lower_frequency,
                higher_frequency,
                threshold,
                roll_off
                ),axis=1)

    print("Next file")
    #TODO: Create a function to make a string to run all of the relevent functions that a user defines in a list. Make it create the new columns in the data frame and run the funtions of the values.
    #TODO: create a function to execute the ae processing algos that we specify in a list. Make it a function.

    # Getting mean and standard deviation of properties and placing in tables.
    normal_mean_processed.loc[file] = processed_data_frame.mean(axis=0)
    normal_std_processed.loc[file] = processed_data_frame.std(axis=0)

# Deleating data frames to free up memory once processing is compleated.
del(file_data_frame)
del(processed_data_frame)

#########################################
# Probability plotting and pdf saving
#########################################

# Adding a prefex to the column headers of mean and std dataframes respectivly used to find correct data later
normal_mean_processed.columns = [f"mean_{col}" for col in normal_mean_processed.columns]
normal_std_processed.columns = [f"std_{col}" for col in normal_std_processed.columns]
combined_normal_mean_std = pd.concat([normal_mean_processed, normal_std_processed], axis=1)

# The pdf file setup
pdf_file_of_charts = PdfPages(Path(pdf_output + "/" + pdf_file_name))

for attribute in properties_to_calculate:
    print(attribute)
    # The apply statement on the data frame to produce the chart
    combined_normal_mean_std .apply(
        lambda row: normal_dis_plot(row[("mean_"+attribute)],row[("std_"+attribute)],row.name), axis=1)
    plt.title(attribute + " normal plots")
    plt.ylabel("Probability")
    plt.xlabel(attribute)
    plt.legend()
    plt.savefig(pdf_file_of_charts,format="pdf")
    plt.clf()

# Close full pdf file.
pdf_file_of_charts.close()