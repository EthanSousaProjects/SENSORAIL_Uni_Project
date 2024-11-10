from Redpitaya_Simplified_Functions import *
from config import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os
import scipy.fft as sci
import math
import redpitaya_scpi as scpi


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
        
            print("Measurement collected (" + fileNamePrefix + ") - " + "Iteration: " + str(iter), " Frequency: " + str(freq) + " Amplitude: " + str(current_amp))

            # Arbitrary delay between measurements
            time.sleep(DELAY_BETWEEN_MEASUREMENTS)

        
        Stop_Signal(REDPITAYA_IP, outChannel)
        Stop_Signal(REDPITAYA_IP, inChannel)
    
        
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


def Quick_Plot(dataframe: pd.DataFrame, samePlot: bool = True, timeDomain: bool = False):
    '''
        Accepts a dataframe formatting identically to the Measure() output and a boolean that dictates whether there are one or multiple plots.\n
        Averages over the iterations and plots the frequency domain against amplitude for each frequency-amplitude pair. 
        Intended to quickly visualise to check for any obvious errors.
    '''
    # Grabbing the unique number of frequency-amplitude combinations
    filteredDataframe = dataframe[dataframe["Iteration"] == 0]
    uniqueCombinations = [filteredDataframe['Excitation Freq'].tolist(), filteredDataframe['Driven Amp'].tolist()]
    numCombinations = len(uniqueCombinations[0]) 

    fig, ax = plt.subplots(1,figsize=(14, 10))  if samePlot else plt.subplots(numCombinations, figsize=(14, 10)) 

    for i in range(numCombinations):
        # Filtering for the frequency
        temp_df = dataframe[dataframe["Excitation Freq"] == uniqueCombinations[0][i]]
        # Filtering for the amplitude
        temp_df = temp_df[temp_df["Driven Amp"] == uniqueCombinations[1][i]]
        # Grabbing the signals
        signals = temp_df["Signal"].tolist()
        # Averaging the signals
        avSignal = np.average(signals, axis=0)
        # Removing DC offset 
        avSignal = avSignal - np.mean(avSignal)

        N = len(avSignal)
        
        if not timeDomain:
            # Grabbing the FFT and freq (excluding the negatives)
            N = len(avSignal)
            FFT = sci.fft(avSignal)
            FFT = FFT[:N // 2]
            freq = sci.fftfreq(N, DT)
            freq = freq[:N // 2]

            # Converting to dB (dBV)
            y = 20*np.log10(FFT) 

            # Plotting
            if not samePlot:
                ax[i].set_title("Excitation Freq: " + str(uniqueCombinations[0][i]) + "Hz, Driven Amp: " + str(uniqueCombinations[1][i]))
                ax[i].grid()
                ax[i].set(xlabel="Frequency (dB)", ylabel="|Amplitude| (dBV)")
                ax[i].semilogx(freq, y)
            else:
                ax.grid()
                ax.set(xlabel="Frequency (dB)", ylabel="|Amplitude| (dBV)")
                ax.semilogx(freq, y, label=str(uniqueCombinations[0][i]) + "Hz" + ", " + str(uniqueCombinations[1][i]) +"V")
                plt.ylim(-3*np.nanmax(y), 3*np.nanmax(y))
                ax.legend()
        else:
            t = [SAMPLING_PERIOD*x for x in range(N)]
            if samePlot:
                ax.plot(t, avSignal, label=str(uniqueCombinations[0][i]) + "Hz" + ", " + str(uniqueCombinations[1][i]) +"V")
                ax.set(xlabel="Time (s)", ylabel="|Amplitude| (dBV)")
                ax.legend()
            else:
                ax[i].plot(t, avSignal)
                ax[i].set(xlabel="Time (s)", ylabel="|Amplitude| (dBV)",  label=str(uniqueCombinations[0][i]) + "Hz" + ", " + str(uniqueCombinations[1][i]) +"V")
                ax[i].legend()
                ax[i].grid()

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