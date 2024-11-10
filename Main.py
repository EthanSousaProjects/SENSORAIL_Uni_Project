'''
Main File to run on raspberry pi.
'''
# Packages to import
from Redpitaya_Simplified_Functions import *
from Higher_Level_Functions import *
import time

[out, red] = Board_Online(REDPITAYA_IP) 
print(out)

if out == True:

    Reset_Signal_All(REDPITAYA_IP)

    type = test_initial["couplant"]

    frequencies = type["f"]
    amplitudes = type["a"]
    fileNamePre = type["n"][0] + type["x"][0]

    # Due to it failing frequently this while loop is required
    success = False
    count = 1
    while success == False:
        print("\nAttempt " + str(count) + "\n")
        try:
            data = Measure(frequencies, amplitudes, DEFAULT_IN, DEFAULT_OUT, True, DEFAULT_ITERATIONS, fileNamePre)
            print("Attempt " + str(count) + " successful.")
            success = True
        except:
            print("Attempt " + str(count) + " failed.")
            count = count + 1
            time.sleep(1)

    # Closed connection before plotting to avoid issues
    Close_Connection(REDPITAYA_IP, red)

    Quick_Plot(data, True)

# Commented-out example of how you would retrieve and plot from a file:
# temp = Get_DF_From_File(DATA_OUT + "/" + "InitTesting_22-55-20.csv")
# Quick_Plot(temp)
