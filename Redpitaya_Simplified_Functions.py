'''
This file will contain functions to interface with the redpitaya board.
Mainly ones for generating and recording signals.
This is simplified to work in the main program.

It will communite using a direct ethernet link.
'''

# Packages to import
import sys
import time
import redpitaya_scpi as scpi

def Board_Online(IP):
    '''
    Function to check if board is online
    IP - The IP address link to the redpitaya board use a "<hostname>.local" address.
    '''
    try:
        rp_s = scpi.scpi(IP)
        status = rp_s.tx_txt(':SYST:ERR?')
        return True

    except:
        # Returned and error board likely off.
        return False


def Start_Continuous_Signal(Freq,Waveform,Amp,IP,Channel_Number):
    '''
    Function to start a signal on a specified output.
    Freq - The frequency which the board should produce
    Waveform - The signal to produce wave form. Options (SINE, SQUARE, TRIANGLE, SAWU,SAWD, PWM, ARBITRARY, DC, DC_NEG)
    Amp - The amplitude of the signal to produce (between 1 and -1).
    IP - The IP address link to the redpitaya board use a "<hostname>.local" address.
    Channel_Number - The output channel number on the redpitaya board (either 1 or 2)
    '''
    rp_s = scpi.scpi(IP)

    # Function for configuring Source (generating signal)
    rp_s.sour_set(Channel_Number, Waveform, Amp, Freq, burst=False)

    # Enable output
    rp_s.tx_txt("OUTPUT" + str(Channel_Number) + ":STATE ON")
    rp_s.tx_txt("SOUR" + str(Channel_Number) + ":TRig:INT")

def Stop_Signal(IP,Channel_Number):
    '''
    Function to stop a specific channels signal.
    IP - The IP address link to the redpitaya board use a "<hostname>.local" address.
    Channel_Number - The output channel number on the redpitaya board (either 1 or 2)
    '''
    scpi.scpi(IP).tx_txt("OUTPUT" + str(Channel_Number) + ":STATE OFF")

def Reset_Signal_All(IP):
    '''
    Function to resart all signal generation on a board
    IP - The IP address link to the redpitaya board use a "<hostname>.local" address.
    '''
    scpi.scpi(IP).tx_txt('GEN:RST')


def Record_Signal(IP,Channel_Number,Decimation):
    '''
    Function to record a signal off one of the input channels
    IP - The IP address link to the redpitaya board use a "<hostname>.local" address.
    Channel_Number - The input channel number on the redpitaya board (either 1 or 2)
    Decimation - Basically setting the sampling rate. 
        See https://redpitaya.readthedocs.io/en/latest/appsFeatures/examples/acquisition/acqRF-samp-and-dec.html 
        Ranges include (1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536)
    '''

    rp_s = scpi.scpi(IP)

    rp_s.tx_txt('ACQ:RST')

    # Function for configuring Acquisition
    # Effectivlyu setting sampling rate
    # See https://redpitaya.readthedocs.io/en/latest/appsFeatures/examples/acquisition/acqRF-samp-and-dec.html for more info
    rp_s.acq_set(Decimation)

    rp_s.tx_txt('ACQ:START')
    time.sleep(0.05)
    rp_s.tx_txt('ACQ:TRig NOW')

    while 1:
        rp_s.tx_txt('ACQ:TRig:STAT?')
        if rp_s.rx_txt() == 'TD':
            break
    
    ## ! OS 2.00 or higher only ! ##
    while 1:
        rp_s.tx_txt('ACQ:TRig:FILL?')
        if rp_s.rx_txt() == '1':
            break

    Signal_Data = rp_s.acq_data(Channel_Number, convert=True)

    return(Signal_Data)

