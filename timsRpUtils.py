"""
This is Tim's utilities for the Red Pitaya STEMlab 125-14

This is a collection of functions I've found very useful. 

"""

import time
import redpitaya_scpi as scpi
import numpy as np
import pandas as pd
import os
from numba import jit
import scipy.stats as stats
import matplotlib.pyplot as plt
from obspy.signal.trigger import aic_simple


def wfmStringToList(_string): return (list(map(float, _string[1:-1].split(','))))

def temperatureStringToList(_string):
    # Remove the brackets and split the string by whitespace
    return list(map(float, _string.strip('[]').split()))


def toms_smoother(sig, win=11):

    """
    Smooth signal using a moving average filter.
    Used for smooth big temperature data

    Replicates MATLAB's smooth function. (http://tinyurl.com/374kd3ny)

    Args:
        sig (np.array): Signal to smooth.
        win (int, optional): Window size. Defaults to 11.
        win must be odd.

    Returns:
        np.array: Smoothed signal.
    """
    out = np.convolve(sig, np.ones(win, dtype=int), 'valid') / win
    r = np.arange(1, win - 1, 2)
    start = np.cumsum(sig[:win - 1])[::2] / r
    stop = (np.cumsum(sig[:-win:-1])[::2] / r)[::-1]
    return np.concatenate((start, out, stop))

def convertVoltsToTemp(_voltage):

    """ 
    This converts a voltage from teh AdaFruit thermo-amp to a temperature reading
    Uses the conversion constants from their datasheet  

    """

    listExample = []

    if type(_voltage) == type(listExample):

        return [((voltage - 1.25)/0.005) for voltage in _voltage]
    
    else:
        return((_voltage - 1.25)/0.005)
    
def convertVoltsToDb(_voltage, _referenceV = 1E-04, _preAmpGain = 40):

    if type(_voltage) ==type(list):
            
            return [20 * np.log10(voltage/_referenceV) - _preAmpGain for voltage in _voltage]
        
    else:

        return 20 * np.log10(_voltage/_referenceV) - _preAmpGain    

def correctTemperature(_temp, _gradient = 0.994669, _offset = 1.519948):

    """ 
    Applys a y=mx+c relationship to correct the temperature reading
    
    Default values are calibrated against Tom's RS51 Digital Thermometer and k type thermocouple
    See tempCalibration1.ipynb for calibration, data, and details

    Parameters:
    _temp: temperature reading to correct
    _gradient: gradient of the line
    _offset: offset of the line

    Returns:
    correctedTemp: corrected temperature reading
    """

    listExample = []

    if type(_temp) == type(listExample):

        return [((temp - _offset)/_gradient) for temp in _temp]
    
    else:

        return (_temp - _offset)/_gradient
    
@jit(nopython=True, cache=True, fastmath=True)
def jitAIC(signal):

    """
    This function calculates the AIC of a signal, used for detecting the arrival time
    It only calculates upto the maximum index of the signal to save on computer time

    Parameters:
    signal: waveform to use must be a np.array

    Returns:
    AIC_Function: AIC values for each point in the signal, upto the maximum index   
    
    """
    minIndex = 1
    maxIndex = np.argmax(signal)

    AIC_Function = []

    AIC_Function.extend([np.nan] * minIndex)

    for k in range(minIndex ,maxIndex-2):
        AIC = (k*np.log(np.var(signal[minIndex-1:k])) 
                + (maxIndex-k-1)*np.log(np.var(signal[k+1:maxIndex])))
        
        AIC_Function.append(AIC)

    AIC_Function.append(np.nan)
    AIC_Function.append(np.nan)

    AIC_Function = [np.nan if np.isinf(aic) else aic for aic in AIC_Function]

    return(np.array(AIC_Function))


class stemLab:
    def __init__(self, _IP = 'rp-f068fb.local'):

        """
        This is a class for setting up your Red Pitaya

        Parameters:
        _IP: IP address of the Red Pitaya, default is 'rp-f068fb.local'

        """

        self.IP = _IP
        self.rp_s = scpi.scpi(self.IP)
        self.BASEFREQ = 125e6
        self.decimation = None
        self.oscillations = None
        self.preTrigSamples = None
        self.actualSampleRate = None

    def normalizeAmplitudes(self, _frequencyList):

        """ 
        This functions normalizes the energy of the input pulses based on their frequency.
        The naturally highest energy pulse is the lowest frequency pulse, so it normalizes 
            the amplitudes against the highest frequency pulse by reducing the amplitudes

        The RP can pulse a maximum of 1V, so the amplitudes are normalized to 0.90V to allow for 
        DC offset

        THE BIGGER THE FREQUENCY, THE SMALLER THE AMPLITUDES

        Parameters:
        _frequencyList: list of the frequencies of the pulses

        Returns:
        desiredAmps: list of the amplitudes to pulse at for each frequency, 
            same size as _frequencyList
        
        """

        lowestFreq = np.min(_frequencyList)
        desiredAmps = []

        for freq in _frequencyList:
            desiredAmps.append(np.sqrt((np.square(1) * freq) / lowestFreq))

        return ((desiredAmps / np.max(desiredAmps)) * 0.75)

    def setPulseRecieveParameters(self, _decimation, _oscillations, _preTrigSamples = 0, _wfmShape = 'SINE'):

        """
        This function sets the parameters for the stemLab to pulse & recieve with

        Parameters:
        _decimation: decimation factor, will result in 125E06/_decimation sample rate
        _oscillations: number of oscillations of the waveform
        _preTrigSamples: number of samples to capture before the trigger, default is 0
        _wfmShape: shape of the waveform, default is 'SINE'        
        
        """

        self.decimation = _decimation
        self.oscillations = _oscillations
        self.preTrigSamples = _preTrigSamples
        self.wfmShape = _wfmShape
        self.actualSampleRate = self.BASEFREQ / self.decimation



    def normalizeAmplitudes(_frequencyList):

        """ 
        This functions normalizes the energy of the input pulses based on their frequency.
        The RP can pulse a maximum of 1V, so the amplitudes are normalized to 0.95V to allow for 
        DC offset

        THE BIGGER THE FREQUENCY, THE SMALLER THE AMPLITUDES

        Parameters:
        _frequencyList: list of the frequencies of the pulses

        Returns:
        desiredAmps: list of the amplitudes to pulse at for each frequency, 
            same size as _frequencyList
        
        """

        lowestFreq = np.min(_frequencyList)
        desiredAmps = []

        for freq in _frequencyList:
            desiredAmps.append(np.sqrt((np.square(1) * freq) / lowestFreq))

        return ((desiredAmps / np.max(desiredAmps)) * 0.95)
    
    def pulseAndRecieve(self, _pulseFreqKHZ, _amplitude = 0.9):

        """
        This function pulses the Red Pitaya at a given frequency and amplitude, and recieves the data

        Parameters:
        _pulseFreqKHZ: frequency of the pulse in kHz
        _amplitude: amplitude of the pulse, default is 0.9

        Returns:
        ch1: data from channel 1
        ch2: data from channel 2

        """


        pulseFreqHz = int(_pulseFreqKHZ * 1000)

        # Confirm the other parameters are set

        if self.decimation == None:
            print('Please set the parameters for the Red Pitaya')
            return
        
        # Setup generator
        self.rp_s.tx_txt('GEN:RST')
        # self.rp_s.tx_txt('GEN:OUT:OFF') 
        self.rp_s.sour_set(1, self.wfmShape, _amplitude, pulseFreqHz, 
                           burst = True, ncyc = int(self.oscillations))
        
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
        time.sleep(0.5)

        return ch1, ch2

    def readGPIOpin(self, _pinNumber):

        """
        This function reads the value of a GPIO pin

        Parameters:
        _pinNumber: number of the pin to read (1, 2, 3, or 4)

        Returns:
        value: value of the pin

        """

        self.rp_s.tx_txt('ANALOG:PIN? AIN' + str(_pinNumber - 1))
        return float(self.rp_s.rx_txt())
    
    def logGPIOAcrossXSeconds(self, _xSeconds = 2, _pinNumber = 2):

        """

        This function logs the value of a GPIO pin across a given number of seconds
        Gets about 21 samples per second

        Parameters:
        _xSeconds: number of seconds to log the data for, default is 2
        _pinNumber: number of the pin to read (1, 2, 3, or 4), default is 2

        Returns:
        timeLog: list of the time values
        voltageLog: list of the voltage values

        """

        timeLog = []
        voltageLog = []
        
        startTime = time.time()
        endTime = startTime + _xSeconds

        while time.time() < endTime:
            timeLog.append(time.time())
            voltageLog.append(self.readGPIOpin(_pinNumber))

        return timeLog, voltageLog
    


class testData:
    def __init__(self, _filePath, _sampleRate = 125E06/16, _sensorSpacing = None, _preTrigSamples = None):

        self.sampleRate = _sampleRate
        self.sensorSpacing = _sensorSpacing
        self.preTrigSamples = _preTrigSamples
        self.timeAxis = None
        
        print("Importing Data from " + _filePath + " ... ")
        self.df = pd.read_csv(_filePath)
        # self.df['waveform'] = self.df['waveform'].apply(wfmStringToList)
        # self.df['waveform'] = self.df['waveform'].apply(lambda x: self.correctDCOffset(x))
        # self.df['temperatureLog'] = self.df['temperatureLog'].apply(temperatureStringToList)
        # self.df['relativeTime'] = self.df['time'] - self.df['time'][0]
        # self.df['time'] = pd.to_datetime(self.df['time'], unit='s').dt.tz_localize('UTC').dt.tz_convert('Europe/London')
        # lengthOfWfm = len(self.df['waveform'][0])
        # self.timeAxis = np.linspace(0, lengthOfWfm/self.sampleRate, lengthOfWfm)
        # del lengthOfWfm
        

        print("Data Imported Succesfully...")


    def getColumnLabels(self):
        self.colLabels = self.df.columns

    def getAverageTemp(self):

        if 'temperatureLog' in self.colLabels:
            self.df['averageTemp'] = self.df['temperatureLog'].apply(lambda x: np.mean(x))

    def correctDCOffset(self, _wfm): return _wfm - np.mean(_wfm)

    def getAE_features(self):

        print("Calcualting AE Features ~ ")

        print("     AIC... ")
        self.df['AIC'] = self.df['waveform'].apply(lambda x: jitAIC(np.array(np.abs(x))))
        # self.df['AIC'] = self.df['AIC'].apply(lambda x: toms_smoother(x, win = 151))

        if self.sensorSpacing != None and self.preTrigSamples != None:
            print("     Arrival Times / Wavespeeds... ")
            self.df['arrivalSample'] = self.df['AIC'].apply(lambda x: np.nanargmin(x))
            self.df['arrivalSample'] = self.df['arrivalSample'] - self.preTrigSamples
            self.df['arrivalTime'] = self.df['arrivalSample'] / self.sampleRate
            self.df['waveSpeed'] = self.sensorSpacing / self.df['arrivalTime']
            self.df.drop(columns=['arrivalSample', 'arrivalTime'], inplace=True)

            self.df['thresholdSpeed'] = self.df['waveform'].apply(lambda x: self.thresholdPicker(np.abs(x)))

 


        print("     Maximum Amplitude... ")
        self.df['maxAmplitude'] = self.df['waveform'].apply(lambda x: np.max(x))

        print("     FFTs... ")
        self.df['FFT'] = self.df['waveform'].apply(lambda x: np.fft.rfft(x))
        self.df['FFT'] = self.df['FFT'].apply(lambda x: np.abs(x))
        self.frequencyAxis = np.fft.rfftfreq(len(self.df['waveform'][0]), d = 1/self.sampleRate)
        self.df['peakFrequency'] = self.df['FFT'].apply(lambda x: self.frequencyAxis[np.argmax(x)])

        print("     Kurtosis and Skew... ")
        self.df['wfmKurtosis'] = self.df['waveform'].apply(lambda x: stats.kurtosis(x))
        self.df['wfmSkew'] = self.df['waveform'].apply(lambda x: stats.skew(x))
        self.df['fftKurtosis'] = self.df['FFT'].apply(lambda x: stats.kurtosis(x))
        self.df['fftSkew'] = self.df['FFT'].apply(lambda x: stats.skew(x))


        ## cross correlation with the first waveform, then correlate it with temperature
        ## also coherence with temperature



    def thresholdPicker(self, wfm, _threshold = 0.05):    

        thresholdCrossing   = np.where(np.abs(wfm) > _threshold)[0][0]
        thresholdCrossing = thresholdCrossing - self.preTrigSamples
        thresholdTime = thresholdCrossing / self.sampleRate
        thresholdSpeed = self.sensorSpacing / thresholdTime

        return thresholdSpeed
    

def inspectWaveform(_wfm, _xlims = None, _ylims = None):

    figure, ax = plt.subplots(2, 1, figsize = (6, 4))

    aicFunc = aic_simple(_wfm)
    maxAmpSample = np.argmax(_wfm)
    aicMin = np.argmin(aicFunc[0:maxAmpSample])

    ax[0].plot(_wfm)
    ax[0].set_title('Waveform')
    ax[0].set_xlabel('Sample')
    ax[0].set_ylabel('Volts')

    ax[0].twinx().plot(aicFunc, color = 'red', alpha = 0.3)
    ax[0].axvline(x = aicMin, color = 'red', linestyle = '--')

    if _xlims != None:
        ax[0].set_xlim(_xlims)

    if _ylims != None:
        ax[0].set_ylim(_ylims)

    ax[1].plot(_wfm)
    ax[1].set_title('Arrival Sample: ' + str(aicMin))
    ax[1].set_xlabel('Sample')
    ax[1].set_ylabel('Volts')
    ax[1].axvline(x = aicMin, color = 'red', linestyle = '--')
    
    ax[1].set_xlim(200, 1600)
    maxAmpInWindow = np.max(_wfm[0:aicMin + 200]) * 1.5
    ax[1].set_ylim(-maxAmpInWindow, maxAmpInWindow)

    plt.tight_layout()

    return figure













        








