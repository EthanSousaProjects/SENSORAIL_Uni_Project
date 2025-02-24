"""

Baseline script to get the gps to output its values. Taken from the adafruit webpage:
https://learn.adafruit.com/adafruit-ultimate-gps/circuitpython-python-uart-usage
on 14th Feb 2025



GPS function that when called sets up the gps module, reads data off it and then returns the longitude and latitude.
If no fix returns 0 for longitude and latitude.
"""
########################
# Packages to import
########################
import time
import board
import busio
import adafruit_gps
import serial

def current_location():
    """
    Returns the current location that the gps module is saying.
    If there is no fix it will return 0,0
 
    Returns:
        longitude: longitude of current location
        latitude: latitude of the current location
    """
    #TODO: Test on pi to be sure it works. Should do though.
    # Creating the serial connection to the GPS
    uart = serial.Serial(board.TX, board.RX, baudrate=9600, timeout=10)

    # Create a GPS module instance to call
    gps = adafruit_gps.GPS(uart, debug=False)  # Use UART/pyserial

    # Initializing the GPS module to send data to the pi and setting up update rate of 1 secound.
    # Turn on the basic GGA and RMC info (what you typically want from a GPS)
    gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
    # Set update rate to once a every second.
    gps.send_command(b"PMTK220,1000")

    # Update GPS data in python
    gps.update()

    if not gps.has_fix:

        print("No fix yet")
        longitude = 0
        latitude = 0

    else:
        # We have a fix! (gps.has_fix is true)
        longitude = gps.longitude
        latitude = gps.latitude

        print("Latitude: {0:.6f} degrees".format(gps.latitude))
        print("Longitude: {0:.6f} degrees".format(gps.longitude))

    # Hopefully stop all GPS communication.
    gps.send_command(b'PMTK314,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')

    return(longitude,latitude)