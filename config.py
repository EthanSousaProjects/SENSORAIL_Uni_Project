import numpy as np;

REDPITAYA_IP = "rp-f06501.local"
DATA_OUT = "data_out"

WAVEFORM = "SINE"
DECIMATION = 32
DEFAULT_ITERATIONS = 3
DELAY_BETWEEN_MEASUREMENTS = 0

DEFAULT_IN = 1
DEFAULT_OUT = 1

SAMPLING_RATE = ((125E6)/DECIMATION)
SAMPLING_PERIOD = 1/SAMPLING_RATE
DT = SAMPLING_PERIOD

# Whether or not the excitation frequency is compensated for in the sampling window, 
# should usually be set to false
NORMALISE_FOR_TIME = False
# Below two are only relevant if the above is true
TOTAL_SAMPLE_TIME = 16384 * SAMPLING_PERIOD
FRACTION_OF_SAMPLING_WINDOW = 0.25

# Whether the amplitudes are normalised across frequencies
NORMALISED_AMP = False
# Factor used. Only relevant if the above is set to true
NORM_AMP_FACTOR = 0.75

DEFAULT_DISTANCE = None
DEFAULT_POSITION = None
DEFAULT_PRE_AMP_GAIN = 40
DEFAULT_OUT_GAIN = 0

DEFAULT_PRE_TRIGGER_SAMPLES = 200
DEFAULT_OSCILLATIONS = 100

# Referenced used for voltage dB calcuations
REFERENCE_VOLTAGE = 1E-4 #100uV

# Delay between samples. Should be at least 0.8 to prevent ringing.
SAMPLING_DELAY = 0.8



# Dict that we can invoke in the Main script while testing
test_initial = dict(

    test = dict(
        f = [20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000, 1000000, 1100000, 1200000],
        a = [1 for i in range(20)],
        n = ["Test"]
    ),
    couplant = dict(
        f = [int(multiplier * 10 ** (decade - 1)) for decade in range(3, int(np.log10(10**6)) + 1) for multiplier in range(2, 10, 2)],
        a = [1 for x in range(20)],
        n = ["None", "Silicon", "Grease", "ThinSilicon"],
        x = ["_Web_Same_Face", "_Web_Head", "_Web_Opp_Face", "_Head_Web"]
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