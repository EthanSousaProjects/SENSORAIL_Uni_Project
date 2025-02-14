"""

Basline motor encoder counter that has been tested to work.

"""
# coding=utf-8
import RPi.GPIO as gpio
gpio.setmode(gpio.BCM)
gpio.setup(17, gpio.IN, pull_up_down=gpio.PUD_UP)
total_pulses=0

def pulse_counter(channel):
    global total_pulses
    total_pulses += 1

gpio.add_event_detect(17, gpio.RISING, callback=pulse_counter) #, bouncetime=0)

import asyncio
import time
start_time = time.time()

async def wait_and_print():
    print("Waiting...")
    await asyncio.sleep(1)  # Wait for 1 seconds
    global start_time
    global start_time
    global total_pulses
    print("Time difference from beginning =", (time.time() - start_time) )
    print("Pulse Total =",total_pulses)

while True:
    # Run the coroutine
    asyncio.run(wait_and_print())
    #print("time difference from beginning=", (time.time() - start_time))
    #print("pulse totoal = ", total_pulses)

