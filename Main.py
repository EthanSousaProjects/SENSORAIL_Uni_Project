'''
Main File to run on raspberry pi.
'''
# Packages to import
from Redpitaya_Simplified_Functions import *
import matplotlib.pyplot as plt

# Constants
Redpitaya_IP = "rp-f06501.local"

# TESTING HERE REMOVE AFTER USE between these comments

# Testing if board is online or not Fase is not online, true is online.
print(Board_Online(Redpitaya_IP))

if Board_Online(Redpitaya_IP) == True:

    Frequency = 50000
    Waveform = "SINE"
    Amplitude = 1
    Channel_Number = 1
    Decimation = 32 # Effectivly sample rate look at charts online.
    # Start Continueos signal
    Start_Continuous_Signal(Frequency,Waveform,Amplitude,Redpitaya_IP,Channel_Number)

    data_Signal = Record_Signal(Redpitaya_IP,Channel_Number,Decimation)
    
    Stop_Signal(Redpitaya_IP,Channel_Number)
    #Reset_Signal_All(Redpitaya_IP)

    data_No_Signal = Record_Signal(Redpitaya_IP,Channel_Number,Decimation)
    
    plt.plot(data_Signal, 'bo')
    plt.plot(data_No_Signal, "r+")
    plt.show()
# TESTING HERE REMOVE AFTER USE between these comments