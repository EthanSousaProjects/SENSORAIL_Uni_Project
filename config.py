import numpy as np;

REDPITAYA_IP = "rp-f06501.local"
DATA_OUT = "data_out"

WAVEFORM = "SINE"
DECIMATION = 32 
DEFAULT_ITERATIONS = 3
DELAY_BETWEEN_MEASUREMENTS = 0

DEFAULT_IN = 1
DEFAULT_OUT = 1

DT = 0.0000001 # Temporary and should really be replaced with a calculation with the decimation

# Dict that we can invoke in the Main script while testing
test_initial = dict(

    couplant = dict(
        f = [int(multiplier * 10 ** (decade - 1)) for decade in range(2, int(np.log10(10**6)) + 1) for multiplier in range(2, 10, 2)],
        a = [1 for x in range(20)],
        n = ["None", "Silicon", "Grease"]
    ),
    positioning = dict(
        f = [int(multiplier * 10 ** (decade - 1)) for decade in range(2, int(np.log10(10**6)) + 1) for multiplier in range(2, 10, 2)],
        a = [1 for x in range(20)],
        n = ["Same_Side_of_Web", "Opposite_Sides_of_Web"]
    ),
    amplitudes = dict(
        f = [10000 for x in range(10)],
        a = [0.1*x for x in range(1,10)],
        n = ["0dB_gain", "XdB_gain" , "..."]
    ),
    amp_over_freq = dict(
        f = [int(multiplier * 10 ** (decade - 1)) for decade in range(2, int(np.log10(10**6)) + 1) for multiplier in range(2, 10, 2)],
        a = [[0.2 for x in range(20)] ,[0.4 for x in range(20)],[0.6 for x in range(20)],[0.8 for x in range(20)], [1 for x in range(20)]],
        n = ["Amp_0.2", "Amp_0.4", "Amp_0.6", "Amp_0.8", "Amp_1"]
    )
)