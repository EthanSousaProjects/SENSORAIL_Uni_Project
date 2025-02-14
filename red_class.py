import sys
import time
import redpitaya_scpi as scpi
from config import *
import ae_process_algos as aepe

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
        self.oscillations = DEFAULT_OSCILLATIONS
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
        
    def set_params(self, decimation = DECIMATION, oscillations = DEFAULT_OSCILLATIONS, preTriggerSamples = DEFAULT_PRE_TRIGGER_SAMPLES, sampling_delay = SAMPLING_DELAY, outChannel = 1,waveformShape = "Sine"):
        '''
        Allows the configuration of individual parameters. Please configure this before creating Dataset objects if you are creating multiple. 
        '''
        
        self.decimation = decimation
        self.oscillations = oscillations
        self.preTrigSamples = preTriggerSamples
        self.waveformShape = waveformShape 
        self.sampling_delay = sampling_delay
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

        oscil = int(self.oscillations)
        print(oscil)
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
        #print(self.decimation)
        self.rp_s.acq_set(dec = self.decimation, trig_delay = (16384/2)-self.preTrigSamples)

        # Start acquisition and generation
        self.rp_s.tx_txt('ACQ:START')
        time.sleep(0.5)
        self.rp_s.tx_txt('ACQ:TRig AWG_PE')
        self.rp_s.tx_txt('OUTPUT1:STATE ON')    
        time.sleep(0.5)
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
        time.sleep(self.sampling_delay)

        return ch1, ch2


class data_set:
    def __init__(self, red: red_class = None, fileName: str = ""): 

        if fileName == "":
            self.red_object = red
            self.df_1 = pd.DataFrame()  # The intention here is to store the last measurement for each channel for easy plotting/analysis
            self.df_2 = pd.DataFrame() 
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
        else:
            # Constructing from a directory
            # Only implemented signal channel as that is all that we'll need
            print("Constructing dataset class from " + fileName)

            data = Get_DF_From_File(fileName)
            direct = fileName.split("/")
            direct[len(direct) - 1] = direct[len(direct) -1].replace("_channel_1_", "").replace("_channel_2_", "")
            label = direct.pop()
            parameters = pd.read_csv("/".join(direct) + "/" + "Parameters__" +label)

            self.red_object = red_class(REDPITAYA_IP)
            self.red_object.set_params( 
                decimation= parameters["Decimation"][0],
                oscillations= parameters["Oscillations"][0],
                preTriggerSamples= parameters["PreTriggerSamples"][0],
                waveformShape= parameters["WaveformShape"][0],
                sampling_delay= parameters["SamplingDelay"][0],
                outChannel= 1,
            )

            self.df_1 = data
            self.set_params(
                dist= parameters["Distance"][0],
                positions= parameters["Postions"][0],
                pre_amp_g = parameters["PreAmpGain"][0],
                out_g= parameters["OutputGain"][0],
                iterations= parameters["Iterations"][0],
                conf= parameters["Configured"][0]
            )

    # set individual parameters
    def set_params(self, iterations = DEFAULT_ITERATIONS,active1 = True, active2=False, dist=DEFAULT_DISTANCE, positions = DEFAULT_POSITION, pre_amp_g = DEFAULT_PRE_AMP_GAIN, out_g = DEFAULT_OUT_GAIN, normalisedAmp = NORMALISED_AMP, conf = True):

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
        self.configured = conf

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
            "Iterations": [self.iterations],
            "Oscillations": [self.red_object.oscillations]
        }
        df = pd.DataFrame().from_dict(d)
        return df
    
    def write_to_disk(self, fileName: str, fileLocation: str= DATA_OUT):
      
        # Creating the directory if it does not exist
        if not os.path.exists(fileLocation):
            os.makedirs(fileLocation)
            
        now = datetime.datetime.now()
        print("Writing to disk: " + fileName)

        if self.channel_1_active:
            self.df_1.to_csv(fileLocation + "/" + fileName + "_channel_1_" + "_" + str(now.hour) + "-" + str(now.minute) + "-" + str(now.second) + ".csv", index=False, header=True)
        if self.channel_2_active:
            self.df_2.to_csv(fileLocation + "/" + fileName + "_channel_1_" + "_" + str(now.hour) + "-" + str(now.minute) + "-" + str(now.second) + ".csv", index=False, header=True)

        self.get_params().to_csv(fileLocation + "/" + "Parameters__" + fileName + "_" + str(now.hour) + "-" + str(now.minute) + "-" + str(now.second) + ".csv", index=False, header=True)

    
    def Measure(self, freq: list[int], amp: list[float], label: str, writeToDisk: bool = True):
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

        self.write_to_disk(fileName=label)

        if self.channel_1_active and self.channel_2_active == False:
            return self.df_1
        else:
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

        return returnFrame, uniqueCombinations
    
 

    def Time_Domain(self, df: pd.DataFrame = pd.DataFrame(), plot:bool=True, averageOrNot:bool = False):

        '''
        Plots a time-domain representation of the data. \n
        '''

        if len(self.df_1) == 0 and len(df) == 0:
            print("No data to plot")
            return
        elif len(df) == 0:
            df = self.df_1
           
        # Checking whether the dataframe is averaged (or a single iteration has been taken)
        averaged = False if len(list(set(df["Iteration"].to_list()))) > 1 else True

        # Allowing the user to average (and centre) at this point
        if averageOrNot and averaged == False:
            df,p = self.ProcessDFForPlotting(df)
        
        # Flawed caclulation -> relies on the 0 index always being present. Need to fix this.
        numCombinations = len([df[df["Iteration"] == 0]['Excitation Freq'].tolist(), df[df["Iteration"] == 0]['Driven Amp'].tolist()][0])

        numIterations = 0
        if numCombinations != 0:
            numIterations = int(len(df)/numCombinations) 
        else:
            numIterations = 1

        # Not actually averaging but getting the unique combinations
        a,uniC = self.ProcessDFForPlotting(df)

        signals = df["Signal"].to_list()
        # Assuming all lengths are the same
        N = len(signals[0])
        t = [(1/self.red_object.actualSampleRate)*x for x in range(N)]


        rows = int(math.ceil(numCombinations/2))
        cols = 2 if numCombinations > 1 else 1
        fig = plt.figure()

        # For each unique combination
        for i in range(numCombinations):

            currentAx = fig.add_subplot(rows, cols, i+1)

            if averaged == False:
                offset = i*numIterations - 1
                for iter in range(numIterations):
                    currentAx.plot(t, signals[offset+ iter], label=str(uniC[0][i]) + "Hz" + ", " + str(uniC[1][i]) +"V, " + str(iter))
                    #currentAx.set(xlabel="Time (s)", ylabel="Amplitude (V)")
                    currentAx.legend(fontsize=5)
                    currentAx.grid()
                fig.suptitle('Time Domain', fontsize=16)
            else:
                currentAx.plot(t, signals[i], label=str(uniC[0][i]) + "Hz" + ", " + str(uniC[1][i]) +"V")
                #currentAx.set(xlabel="Time (s)", ylabel="Amplitude (V)")
                currentAx.legend(fontsize = 5)
                currentAx.grid()
                fig.suptitle('Time Domain - Averaged/Single', fontsize=16)

        
        
        if plot:
            plt.show()
        else:
            plt.ioff() 
       
        return fig
    

    def Frequency_Domain(self, df: pd.DataFrame = pd.DataFrame(), plot:bool=True):

        '''
        Plots frequency-domain representation of the data. \n
        '''

        if len(self.df_1) == 0 and len(df) == 0:
            print("No data to plot")
            return
        elif len(df) == 0:
            df = self.df_1
 
        fig, ax = plt.subplots()
        signals = df["Signal"].to_list()
        freqList = df["Excitation Freq"].to_list()
        ampList = df["Driven Amp"].to_list()
        iterList = df["Iteration"].to_list()

        for i in range(len(signals)):
            
            avSignal = signals[i] - np.mean(signals[i])
            N = len(avSignal)
            FFT = abs(np.fft.rfft(avSignal))
            freq = np.fft.rfftfreq(N, 1/(125E6/self.red_object.decimation))/1E3
        

            # Converting to dB (dBV)
            y = 20*np.log10(FFT/REFERENCE_VOLTAGE) #- self.pre_amp_gain
    
            ax.grid()
            ax.set(xlabel="Frequency (kHz)", ylabel="|Amplitude| (V)") #ylabel="|Amplitude| (dBuV)
            ax.plot(freq, FFT, label=str(freqList[i]/1E3) + " kHz" + ", " + str(ampList[i]) +"V" + ", " + str(iterList[i]))
            #plt.ylim(0,)
            ax.legend(fontsize=5)

        fig.suptitle('Frequency Domain', fontsize=16)

        if plot:
            plt.show()
        else:
            plt.ioff() 
       

        return fig
    

    def SNR(self, df:pd.DataFrame = pd.DataFrame(), plot:bool=True):
        '''
        Calculates the Signal to Noise Ratio for the dataset by comparing the average power of the pre-trigger \n
        samples to the post-trigger samples. 
        '''

        if len(self.df_1) == 0 and len(df) == 0:
            print("No data to plot")
            return
        elif len(df) == 0:
            df = self.df_1
           

        signals = df["Signal"].tolist()
        SNR_array = []

        

        for i in range (len(signals)):
            sig = signals[i]

            # Be careful here as passing in a dataframe might actually result in the wrong pre-trigger samples being used
            pre_trigger_signal = sig[:self.red_object.preTrigSamples]
            post_trigger_signal = sig[self.red_object.preTrigSamples:] 
           
            # Calculating the power
            pre_trigger_power = np.sum(np.square(pre_trigger_signal))/len(pre_trigger_signal)
            post_trigger_power = np.sum(np.square(post_trigger_signal))/len(post_trigger_signal)

            # Calculating the SNR in dB
            SNR = 10*np.log10(post_trigger_power/pre_trigger_power)
            SNR_array.append(SNR)
        
        fig, ax = plt.subplots()
        outArr = np.transpose([df["Excitation Freq"].tolist(), df["Driven Amp"].tolist(),df["Iteration"].tolist(),[snr for snr in SNR_array]]).tolist()
        ax.table(cellText=outArr, loc='center', colLabels=["Frequency (Hz)", "Amplitude (V)", "Iteration","SNR (dB)"])
            
        if plot:
            plt.show()
        else:
            plt.ioff()

        return fig

    def Quick_Plot_New():
        # Will add a comprehensive quick plot function that uses a tabbed window to essentially plot everything
        # Will leverage the stored dataframes from previous measurements to make the function calls as easy as possible
        pass


    def features(self, df = pd.DataFrame(),lowF = DEFAULT_LOWER_FREQUENCY, highF = DEFAULT_HIGHER_FREQUENCY, thresh = DEFAULT_THRESHOLD, rollOff = DEFAULT_ROLL_OFF):
        def computeFeatures(row):
                sig = np.array(row["Signal"]) 
                feat = aepe.compute_all_ae_processing_algos(sig, 125E6/self.red_object.decimation, lowF, highF, thresh, rollOff)
                return pd.Series(feat)
        
        if len(df) == 0:    
            if self.df_1.empty:
                print("DataFrame is empty.")
                return
    
            features_df = self.df_1.apply(computeFeatures, axis=1)
            self.df_1 = pd.concat([self.df_1, features_df], axis=1)
        
            return features_df
        else:
            features_df = df.apply(computeFeatures, axis=1)
            df = pd.concat([df, features_df], axis=1)
            return features_df
        

    def average_features_over_iterations(self, df = pd.DataFrame()):

        if len(df) == 0:
            df = self.df_1

        featuresDF = self.features()
        a, uniC = self.ProcessDFForPlotting(df)

        exportFrame = pd.DataFrame()

        for x in range(len(uniC[0])):
            filtered = df[(df["Excitation Freq"] == uniC[0][x]) & (df["Driven Amp"] == uniC[1][x])]
            av_feat_df = pd.DataFrame()

            av_feat_df["Excitation Freq"] = [uniC[0][x]]
            av_feat_df["Driven Amp"] =[ uniC[1][x]]

            for feat in PROPERTIES_TO_CALCULATE:
                av_feat_df[feat] = [np.mean(filtered[feat])]
            
            exportFrame = pd.concat([exportFrame, av_feat_df], ignore_index=True)
            
        return exportFrame