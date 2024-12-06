import sys
import time
import redpitaya_scpi as scpi
from config import *

import matplotlib.pyplot as plt
import pandas as pd
import scipy.fft as sci
import os
import math
import datetime
from Higher_Level_Functions import Get_DF_From_File, get_most_recent_csv


class red_class:
    def __init__(self, IP = REDPITAYA_IP):
        self.IP = IP
        self.decimation = DECIMATION
        self.actualSampleRate = 125E6/self.decimation
        self.sampling_delay = SAMPLING_DELAY
        self.preTrigSamples = DEFAULT_PRE_TRIGGER_SAMPLES
        self.waveformShape = WAVEFORM
        self.outChannel = DEFAULT_OUT
        self.normalised_amp_factor = NORM_AMP_FACTOR

        try:
            self.rp_s = scpi.scpi(self.IP)
            status = self.rp_s.tx_txt(':SYST:ERR?')
            print("Connected to Board.")
        except:
            print("Cannot Connect to Board.")
        
    def set_params(self, decimation = DECIMATION, oscillations = DEFAULT_OSCILLATIONS, preTriggerSamples = DEFAULT_PRE_TRIGGER_SAMPLES, outChannel = 1,waveformShape = "Sine"):
        '''
        Allows the configuration of individual parameters. Please configure this before creating Dataset objects if you are creating multiple. 
        '''
        
        self.decimation = decimation
        self.oscillations = oscillations
        self.preTrigSamples = preTriggerSamples
        self.waveformShape = waveformShape 
        self.outChannel = outChannel
        self.actualSampleRate = 125E6/self.decimation
        # Need to update


    def norm_amps(self, freq, amp):
        '''
        Provides functionality to normalise ampliudes across frequencies. Do not use directly.
        '''
        lowestFreq = np.min(freq)
        desiredAmps = []


        for f in freq:
            desiredAmps.append(np.sqrt(((np.square(1) * f) / lowestFreq)))

        return np.round(((desiredAmps / np.max(desiredAmps)) * NORM_AMP_FACTOR * amp), 3)
    
    # Sending a particular number of oscillations of a particlar frequency at a particular amplitude
    def pulseAndRecieve(self, out_channel, pulseFreqKHZ, amplitude):

        """
        Stolen almost entirely from Tim's code.
        This function pulses the Red Pitaya at a given frequency and amplitude, and recieves the data

        Parameters:
        _pulseFreqKHZ: frequency of the pulse in kHz
        _amplitude: amplitude of the pulse, default is 0.9

        Returns:
        ch1: data from channel 1
        ch2: data from channel 2

        """

        oscil = int(DEFAULT_OSCILLATIONS)
        pulseFreqHz = int(pulseFreqKHZ * 1000)
        if NORMALISE_FOR_TIME:
            oscil = int(TOTAL_SAMPLE_TIME * FRACTION_OF_SAMPLING_WINDOW/ (1/pulseFreqHz))
        

        # Confirm the other parameters are set

        if self.decimation == None:
            print('Please set the parameters for the Red Pitaya')
            return
        
        # Setup generator
        self.rp_s.tx_txt('GEN:RST')
        # self.rp_s.tx_txt('GEN:OUT:OFF') 
        self.rp_s.sour_set(out_channel, self.waveformShape, amplitude, pulseFreqHz, 
                           burst = True, ncyc = int(oscil))
        
        # Setup Acquisition
        self.rp_s.tx_txt('ACQ:RST')
        self.rp_s.acq_set(dec = self.decimation, trig_delay = (16384/2)-self.preTrigSamples)

        # Start acquisition and generation
        self.rp_s.tx_txt('ACQ:START')
        self.rp_s.tx_txt('ACQ:TRig AWG_PE')
        self.rp_s.tx_txt('OUTPUT1:STATE ON')    
        self.rp_s.tx_txt('SOUR1:TRig:INT')
        self.rp_s.tx_txt('SOUR2:TRig:INT')

        # I have no idea what this does - Tim
        ## ! OS 2.00 or higher only ! ## 
        while 1:
            self.rp_s.tx_txt('ACQ:TRig:FILL?')
            if self.rp_s.rx_txt() == '1':
                break

        # Read data from buffer
  
        ch1 = self.rp_s.acq_data(1, convert= True)
        ch2 = self.rp_s.acq_data(2, convert= True) 

        # Stop the generator
        self.rp_s.tx_txt('OUTPUT1:STATE OFF')
        self.rp_s.tx_txt('OUTPUT2:STATE OFF')

        # Wait time is recommended
        time.sleep(SAMPLING_DELAY)

        return ch1, ch2


        plt.show()


class data_set:
    def __init__(self, red: red_class = None): 

        # Need to add the option to contruct the class purely off of a filename, enabling complete retrieval 
        # from the disk 

        self.red_object = red
        self.df_1 = None  # The intention here is to store the last measurement for each channel for easy plotting/analysis
        self.df_2 = None
        self.configured = False # Bool that is indicative of whether the set_params function has been used, 
                                # allowing for a quick and easy answer to "did I configure that or did I just leave it on the defaults?"

        self.distance = DEFAULT_DISTANCE # Distance between the sensors
        self.positions = DEFAULT_POSITION # Positions of the sensors
        self.pre_amp_gain = DEFAULT_PRE_AMP_GAIN 
        self.output_gain = DEFAULT_OUT_GAIN # Gain applied to the output. This should be reserved for power gain

        self.normalisedAmp = NORMALISED_AMP # Whether the amplitudes are normalised or not. 

        self.iterations = DEFAULT_ITERATIONS # How many iterations this datasets goes through

        # Defining which input channels are active. 
        self.channel_1_active = True
        self.channel_2_active = False

    # set individual parameters
    def set_params(self, iterations = DEFAULT_ITERATIONS,active1 = True, active2=False, dist=DEFAULT_DISTANCE, positions = DEFAULT_POSITION, pre_amp_g = DEFAULT_PRE_AMP_GAIN, out_g = DEFAULT_OUT_GAIN, normalisedAmp = NORMALISED_AMP):

        '''
        Enables the setting of individual parameters pertaining to the measurement set. Use the embedded red_object to configure the other parameters.
        '''

        self.distance = dist
        self.positions = positions
        self.pre_amp_gain = pre_amp_g
        self.output_gain = out_g

        self.normalisedAmp = normalisedAmp
        self.iterations = iterations

        self.channel_1_active = active1
        self.channel_2_active = active2

        # To be able to verify if configuration was done or were default parameters relied upon
        self.configured = True  

    def get_params(self):

        '''
        Function to retrieve the parameters. Currently used to write the parameters to a file upon measurement but can be used to quickly view the parameters. 
        '''

        d = {
            "Configured": [self.configured],
            "Distance": [self.distance],
            "Postions": [self.positions],
            "OutputGain": [self.output_gain],
            "Decimation": [self.red_object.decimation],
            "SamplingRate": [(125E6/self.red_object.decimation)],
            "SamplingDelay": [self.red_object.sampling_delay],
            "PreTriggerSamples": [self.red_object.preTrigSamples],
            "WaveformShape":[self.red_object.waveformShape],
            "NormalisedAmpFactor": [self.red_object.normalised_amp_factor],
            "PreAmpGain": [self.pre_amp_gain],
            "NormalisedAmp": [self.normalisedAmp],
            "Iterations": [self.iterations]
        }
        df = pd.DataFrame().from_dict(d)
        return df
    
    def write_to_disk(self, df_x: pd.DataFrame, fileName: str, fileLocation: str= DATA_OUT,param: bool = False):
      
        # Creating the directory if it does not exist
        if not os.path.exists(fileLocation):
            os.makedirs(fileLocation)
            
        now = datetime.datetime.now()
        print("Writing to disk: " + fileName)

        # Prefixes parameter files 
        prefix = "Parameters__" if param else ""
        df_x.to_csv(fileLocation + "/" + prefix + fileName + "_" + str(now.hour) + "-" + str(now.minute) + "-" + str(now.second) + ".csv", index=False, header=True)
        


    
    def Measure(self, freq: list[int], amp: list[float], label: str):
        '''
        Principle function that carries out the measurement using the pulse and receive function.
        Functions almost identically to the previous iteration and accomodates both channels.
        '''

        # You likely also want a "measure baseline function" to get the noise floor of those particular coupling conditions
        if NORMALISED_AMP:
            amp = self.red_object.norm_amps(freq, amp)
        
        chan1_data = []
        chan2_data = []

        if len(freq) != len(amp):
            print("Frequency-Amplitude length disparity")
            return -1
        
        for i in range(len(freq)):

            f = freq[i]
            a = amp[i]

            for iter in range(self.iterations):
                [sig1, sig2] = self.red_object.pulseAndRecieve(self.red_object.outChannel, f/1000, a)
                now = datetime.datetime.now()

                chan1_data.append([f, iter, a, now.time(), sig1])
                chan2_data.append([f, iter, a, now.time(), sig2])

                print("Measurement collected (" + label + ") - " + "Iteration: " + str(iter), " Frequency: " + str(f) + " Amplitude: " + str(a))
        
        self.df_1 = pd.DataFrame(chan1_data, columns=["Excitation Freq", "Iteration", "Driven Amp", "Time", "Signal"])
        self.df_2 = pd.DataFrame(chan2_data, columns=["Excitation Freq", "Iteration", "Driven Amp", "Time", "Signal"])

        if self.channel_1_active:
            self.write_to_disk(self.df_1, label + "_channel_1_")
        if self.channel_2_active:
            self.write_to_disk(self.df_2, label + "_channel_2_")

        self.write_to_disk(self.get_params(), label, param=True)
    
        return self.df_1, self.df_2
    
    
    def ProcessDFForPlotting(self, df: pd.DataFrame):

        '''
        Averaging, removing DC offset
        '''
        
        filteredDataframe = df[df["Iteration"] == 0]
        uniqueCombinations = [filteredDataframe['Excitation Freq'].tolist(), filteredDataframe['Driven Amp'].tolist()]
        numCombinations = len(uniqueCombinations[0]) 

        returnFrame = pd.DataFrame(columns=df.columns)

        for i in range(numCombinations):
            # Filtering for the frequency
            temp_df = df[df["Excitation Freq"] == uniqueCombinations[0][i]]
            # Filtering for the amplitude
            temp_df = temp_df[temp_df["Driven Amp"] == uniqueCombinations[1][i]]
            # Grabbing the signals
            signals = temp_df["Signal"].tolist()
            # Averaging the signalsds
            avSignal = np.average(signals, axis=0)
            # Removing DC offset 
            avSignal = avSignal - np.mean(avSignal)

            newRow = {
                "Excitation Freq": uniqueCombinations[0][i],
                "Iteration": 0,
                "Driven Amp": uniqueCombinations[1][i],
                "Time": filteredDataframe['Time'].to_list()[i],
                "Signal": avSignal
            }

            returnFrame.loc[len(returnFrame)] = newRow
        print(returnFrame)
        return returnFrame, uniqueCombinations
    
    # Will be deprecated soon. 
    # Does not work comprehensively 
    def Quick_Plot(self, dataframe: pd.DataFrame = pd.DataFrame(), samePlot: bool = True, timeDomain: bool = False):
        
        '''
            Accepts a dataframe formatting identically to the Measure() output and a boolean that dictates whether there are one or multiple plots.\n
            Averages over the iterations and plots the frequency domain against amplitude for each frequency-amplitude pair. 
            Intended to quickly visualise to check for any obvious errors.
        '''

        # Needs to accomodate both channels and retrieval from class member properties
        
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
            # Averaging the signalsds
            avSignal = np.average(signals, axis=0)
            # Removing DC offset 
            avSignal = avSignal - np.mean(avSignal)

            
            
            if not timeDomain:
                # Grabbing the FFT and freq (excluding the negatives)
                N = len(avSignal)
                FFT = np.fft.rfft(avSignal)
                FFT = FFT[:N // 2]
                freq = np.fft.rfftfreq(N, DT)
                freq = freq[:N // 2]

                # Converting to dB (dBV)
                y = 20*np.log10(FFT/REFERENCE_VOLTAGE) - DEFAULT_PRE_AMP_GAIN
        
                # Plotting
                if not samePlot:
                    ax[i].set_title("Excitation Freq: " + str(uniqueCombinations[0][i]) + "Hz, Driven Amp: " + str(uniqueCombinations[1][i]))
                    ax[i].grid()
                    ax[i].set(xlabel="", ylabel="")
                    ax[i].semilogx(freq, y)
                    #plt.title(" |Amplitude| (dBuV) vs Frequency (Hz) ")
                else:
                    ax.grid()
                    ax.set(xlabel="Frequency", ylabel="|Amplitude| (dBuV)")
                    ax.semilogx(freq, y, label=str(uniqueCombinations[0][i]) + "Hz" + ", " + str(uniqueCombinations[1][i]) +"V")
                    # plt.ylim(2*np.nanmax(y), 2*np.nanmax(y))
                    ax.legend()
            else:
                N = len(avSignal)
                t = [SAMPLING_PERIOD*x for x in range(N)]
                if samePlot:
                    ax.plot(t, avSignal, label=str(uniqueCombinations[0][i]) + "Hz" + ", " + str(uniqueCombinations[1][i]) +"V")
                    ax.set(xlabel="Time (s)", ylabel="Amplitude (V)")
                    ax.legend()
                else:
                    ax[i].plot(t, avSignal, label=str(uniqueCombinations[0][i]) + "Hz" + ", " + str(uniqueCombinations[1][i]) +"V" )
                    ax[i].set(xlabel="", ylabel="")
                    ax[i].legend()
                    ax[i].grid()

        plt.show()
    
        return fig, ax
    
   
        

    def Time_Domain(self, df: pd.DataFrame, plot:bool=True, averageOrNot:bool = False):

        '''
        Plots a time-domain representation of the data. \n
        averageOrNot applied the ProcessDFForPlotting function.
        '''

        # Checking whether the dataframe is averaged (or a single iteration has been taken)
        averaged = False if len(list(set(df["Iteration"].to_list()))) > 1 else True

        # Allowing the user to average (and centre) at this point
        if averageOrNot and averaged == False:
            df,p = self.ProcessDFForPlotting(df)
        
        numCombinations = len([df[df["Iteration"] == 0]['Excitation Freq'].tolist(), df[df["Iteration"] == 0]['Driven Amp'].tolist()][0])
        numIterations = int(len(df)/numCombinations)

        # Not actually averaging but getting the unique combinations
        a,uniC = self.ProcessDFForPlotting(df)

        signals = df["Signal"].to_list()
        # Assuming all lengths are the same
        N = len(signals[0])
        t = [(1/self.red_object.actualSampleRate)*x for x in range(N)]


        rows = int(math.ceil(numCombinations/2))
        fig = plt.figure()

        # For each unique combination
        for i in range(numCombinations):

            currentAx = fig.add_subplot(rows, 2, i+1)

            if averaged == False:
                offset = i*numIterations - 1
                for iter in range(numIterations):
                    currentAx.plot(t, signals[offset+ iter], label=str(uniC[0][i]) + "Hz" + ", " + str(uniC[1][i]) +"V, " + str(iter))
                    #currentAx.set(xlabel="Time (s)", ylabel="Amplitude (V)")
                    currentAx.legend()
                fig.suptitle('Time Domain', fontsize=16)
            else:
                currentAx.plot(t, signals[i], label=str(uniC[0][i]) + "Hz" + ", " + str(uniC[1][i]) +"V")
                #currentAx.set(xlabel="Time (s)", ylabel="Amplitude (V)")
                currentAx.legend()
                fig.suptitle('Time Domain - Averaged', fontsize=16)

        
        
        if plot:
            plt.show()

        return fig
        

    def Frequency_Domain(self, df: pd.DataFrame, plot:bool=True):

        '''
        Plots a time-domain representation of the data. \n
        averageOrNot applied the ProcessDFForPlotting function.
        '''

        averaged = False if len(list(set(df["Iteration"].to_list()))) > 1 else True

        # You wouldn't want a non-averaged frequency spectrum plot, right?
        if averaged == False:
            df, uniC = self.ProcessDFForPlotting(df)
        else:
            a, uniC = self.ProcessDFForPlotting(df)

        fig, ax = plt.subplots()
        signals = df["Signal"].to_list()

        for i in range(len(signals)):
            
            avSignal = signals[i]
            N = len(avSignal)
            FFT = np.fft.rfft(avSignal)
            FFT = FFT[:N // 2]
            freq = np.fft.rfftfreq(N, DT)
            freq = freq[:N // 2]

            # Converting to dB (dBV)
            y = 20*np.log10(FFT/REFERENCE_VOLTAGE) - DEFAULT_PRE_AMP_GAIN
    
            ax.grid()
            ax.set(xlabel="Frequency", ylabel="|Amplitude| (dBuV)")
            ax.semilogx(freq, y, label=str(uniC[0][i]) + "Hz" + ", " + str(uniC[1][i]) +"V")
            # plt.ylim(2*np.nanmax(y), 2*np.nanmax(y))
            ax.legend()

        fig.suptitle('Frequency Domain', fontsize=16)

        if plot:
            plt.show()


        return fig


    def Quick_Plot_New():
        # Will add a comprehensive quick plot function that uses a tabbed window to essentially plot everything
        # Will leverage the stored dataframes from previous measurements to make the function calls as easy as possible
        pass