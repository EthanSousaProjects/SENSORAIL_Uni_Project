'''
Main File to run on raspberry pi.
'''
# Packages to import
from Redpitaya_Simplified_Functions import *
from Higher_Level_Functions import *
import matplotlib.pyplot as plt


print(Board_Online(REDPITAYA_IP))

if Board_Online(REDPITAYA_IP) == True:

    Reset_Signal_All(REDPITAYA_IP)

    # Input lists assumed to correspond 1:1
    frequencies = [10000, 20000, 30000, 10000, 20000, 30000]
    amplitudes = [1, 1, 1, 0.5, 0.5, 0.5]

    data = Measure(frequencies, amplitudes, 1, 1, True, 10, "InitTesting")
    Quick_Plot(data)

# Commented-out example of how you would retrieve and plot from a file:
# temp = Get_DF_From_File(DATA_OUT + "/" + "InitTesting_22-55-20.csv")
# Quick_Plot(temp)

    