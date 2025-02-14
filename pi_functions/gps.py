"""

Baseline script to get the gps to output its values. Taken from the adafruit webpage:
https://learn.adafruit.com/adafruit-ultimate-gps/circuitpython-python-uart-usage
on 14th Feb 2025



Simple GPS module demonstration.
Will wait for a fix and print a message every second with the current location
and other details.
"""
########################
# Packages to import
########################
import time
import board
import busio
import adafruit_gps
import serial

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

else:
    # We have a fix! (gps.has_fix is true)
    # Print out details about the fix like location, date, etc.
    print(
        "Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}".format(
            gps.timestamp_utc.tm_mon,  # Grab parts of the time from the
            gps.timestamp_utc.tm_mday,  # struct_time object that holds
            gps.timestamp_utc.tm_year,  # the fix time.  Note you might
            gps.timestamp_utc.tm_hour,  # not get all data like year, day,
            gps.timestamp_utc.tm_min,  # month!
            gps.timestamp_utc.tm_sec,
        )
    )
    print("Latitude: {0:.6f} degrees".format(gps.latitude))
    print("Longitude: {0:.6f} degrees".format(gps.longitude))
    print(
        "Precise Latitude: {} degs, {:2.4f} mins".format(
            gps.latitude_degrees, gps.latitude_minutes
        )
    )
    print(
        "Precise Longitude: {} degs, {:2.4f} mins".format(
            gps.longitude_degrees, gps.longitude_minutes
        )
    )
    print("Fix quality: {}".format(gps.fix_quality))
    # Some attributes beyond latitude, longitude and timestamp are optional
    # and might not be present.  Check if they're None before trying to use!
    if gps.satellites is not None:
        print("# satellites: {}".format(gps.satellites))
    if gps.altitude_m is not None:
        print("Altitude: {} meters".format(gps.altitude_m))
    if gps.speed_knots is not None:
        print("Speed: {} knots".format(gps.speed_knots))
    if gps.speed_kmh is not None:
        print("Speed: {} km/h".format(gps.speed_kmh))
    if gps.track_angle_deg is not None:
        print("Track angle: {} degrees".format(gps.track_angle_deg))
    if gps.horizontal_dilution is not None:
        print("Horizontal dilution: {}".format(gps.horizontal_dilution))
    if gps.height_geoid is not None:
        print("Height geoid: {} meters".format(gps.height_geoid))

# Hopefully stop all GPS communication.
gps.send_command(b'PMTK314,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')