'''
Main File to run on raspberry pi.
'''
# Packages to import
from Redpitaya_Simplified_Functions import *
from Higher_Level_Functions import *
import time
import numpy as np
import matplotlib.pyplot as plt
from red_class import *


rp = red_class(REDPITAYA_IP)
ds = data_set(rp)

#freq = [20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000, 1000000, 1100000, 1200000]
freq = [20000, 30000, 40000]
amp = [0.5 for i in range(len(freq))]

ds.set_params(active1=True, active2=True)

df = Get_DF_From_File("data_out/Grease_Web_Same_Face_40dB__12-49-0.csv")
#df = Get_DF_From_File("data_out/FirstSweep1V_19-16-33.csv")

ds.Time_Domain(df)
#ds.Frequency_Domain(df)

# df_1, df_2 = ds.Measure(freq, amp, label="Noise_Test_2")
# ds.Time_Domain(df_1)

# ds.df_1 = ds.df_1[ds.df_1["Excitation Freq"] == 10]
# ds.Time_Domain(df_1)

# =======================================================
# Soon to add a comprehensive, tabbed Quick_Plot successor.
# =======================================================



