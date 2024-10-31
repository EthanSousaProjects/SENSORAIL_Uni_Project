from Redpitaya_Simplified_Functions import *
from config import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os
import scipy.fft as sci
import math

import ast


def Measure(eFreq: list[int],
            amp: list[float], 
            inChannel: int, 
            outChannel: int, 
            writeToDisk: bool = False,
            numIterations: int = DEFAULT_ITERATIONS,
            fileNamePrefix: str = "",
):
    '''
        Handles the process of measurement entirely. Leans on constants defined in config.py. Returns a dataframe of the data. \n
        eFreq = excitation frequencies as a list \n
        amp = driven amplitudes as a list \n
        inChannel = input channel \n
        outChannel = output channel \n
        writeToDisk = dictates whether the data is written to the disk \n
        fileNamePrefix = allowing a custom string to be in the filename
    '''
    
    # Assumes the board is online
    
    # Initialising the 2D list 
    outList = []

    # Checking if the input lists are of equal length
    if len(eFreq) != len(amp):
        return -1
    
    # Iterating through each freq and amp
    for i in range(len(eFreq)):

        freq = eFreq[i]
        current_amp = amp[i]

        # Iterating
        for iter in range(numIterations):
    
            # Starting the signal, collecting the data, and stopping the signal
            Start_Continuous_Signal(freq, WAVEFORM, current_amp, REDPITAYA_IP,outChannel)
            sig = Record_Signal(REDPITAYA_IP, inChannel, DECIMATION)
            Stop_Signal(REDPITAYA_IP, outChannel)

            # Appending the data to the output list
            now = datetime.datetime.now()
            outList.append([freq, iter, current_amp, now.time(), sig])
        
            print("Measurement collected - " + "Iteration: " + str(iter), " Frequency: " + str(freq) + " Amplitude: " + str(current_amp))

            # Arbitrary delay between measurements
            time.sleep(DELAY_BETWEEN_MEASUREMENTS)

        Stop_Signal(REDPITAYA_IP, outChannel) # Wasn't stopping consistently so I tried this 
        
    # Creating the output dataframe
    df = pd.DataFrame(outList, columns=["Excitation Freq", "Iteration", "Driven Amp", "Time", "Signal"])

    # Writing to disk
    if writeToDisk:
        # Creating the directory if it does not exist
        if not os.path.exists(DATA_OUT):
            os.makedirs(DATA_OUT)

        print("Writing to disk")
        df.to_csv(DATA_OUT + "/" + fileNamePrefix + "_" + str(now.hour) + "-" + str(now.minute) + "-" + str(now.second) + ".csv", index=False, header=True)
        
            
    return df


def Quick_Plot(dataframe: pd.DataFrame):
    '''
        Accepts a dataframe formatting identically to the Measure() output. \n
        Averages over the iterations and plots the frequency domain against amplitude for each frequency-amplitude pair. 
        Intended to quickly visualise to check for any obvious errors.
    '''
    # Grabbing the unique number of frequency-amplitude combinations
    filteredDataframe = dataframe[dataframe["Iteration"] == 0]
    uniqueCombinations = [filteredDataframe['Excitation Freq'].tolist(), filteredDataframe['Driven Amp'].tolist()]
    numCombinations = len(uniqueCombinations[0]) 

    #fig, ax = plt.subplots(math.ceil(math.sqrt(numCombinations)),math.ceil(math.sqrt(numCombinations)),figsize=(14, 10))
    fig, ax = plt.subplots(numCombinations,figsize=(14, 10))

    for i in range(numCombinations):
        # Filtering for the frequency
        temp_df = dataframe[dataframe["Excitation Freq"] == uniqueCombinations[0][i]]
        # Filtering for the amplitude
        temp_df = temp_df[temp_df["Driven Amp"] == uniqueCombinations[1][i]]
        # Grabbing the signals
        signals = temp_df["Signal"].tolist()
        # Averaging the signals
        avSignal = np.average(signals, axis=0)

        N = len(avSignal)
        
        # Grabbing the FFT and freq (excluding the negatives)
        FFT = sci.fft(avSignal)
        FFT = FFT[:N // 2]
        freq = sci.fftfreq(N, DT)
        freq = freq[:N // 2]

        # Converting to dB
        y = 10*np.log10(np.abs(FFT))

        # Plotting
        ax[i].set_title("Excitation Freq: " + str(uniqueCombinations[0][i]) + "Hz, Driven Amp: " + str(uniqueCombinations[1][i]))
        ax[i].grid()
        ax[i].set(xlabel="Frequency (dB)", ylabel="|Amplitude| (dB)")
        ax[i].semilogx(freq, y)

    plt.show()
    

def Get_DF_From_File(filename: str):
    
    '''
        Accepts a filename. Returns a correctly formatted dataframe from a file. 
    '''

    # Reading df
    df = pd.read_csv(filename)
    # Converting the "Signal" column to a list of floats
    df['Signal'] = df['Signal'].apply(lambda x: list(map(float, ast.literal_eval(x))) if pd.notnull(x) else [])
    
    return df