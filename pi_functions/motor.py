"""

Class to manage things with a motor and the encoder outputs.

Defines distance traveled and and on and off function for manual movements.
"""
import RPi.GPIO as gpio
from sys import exit

#TODO: Finish making this motor class See description on what has to be made.
#TODO: double check all comments/ doc strings are formatted + described correctly.
#TODO: Test class works as i expect.
class pololu_motor:
    """
        A class to manage the pololu motors and their encoders.
        The basic class setup will contain functions to set the motors power and rotation direction (A or B)

        The advanced setup will move the bot a set distance based on setup parameters. Run <object name>.encode_pins and <object name>.dis_setup to finished advanced setup.

        Args:
            power: the pwm pin that sets the power of the motor
            dir_a: The gpio pin which defines if the motor will rotate in the A direction (clockwise/ anti) opposite to B direction
            dir_b: The gpio pin which defines if the motor will rotate in the B direction (clockwise/ anti) opposite to A direction
            encode_num: The number of encoders that will be used. Option of just using one of them or both (only input 1 or 2)

    """
    #TODO: Finish off writing the comment above so that the usage of the class is clear.
    def _init_(power,dir_a,dir_b,encode_num):
        """
        Parameters needed when setting up the class

        Args:
            power: the pwm pin that sets the power of the motor
            dir_a: The gpio pin which defines if the motor will rotate in the A direction (clockwise/ anti) opposite to B direction
            dir_b: The gpio pin which defines if the motor will rotate in the B direction (clockwise/ anti) opposite to A direction
            encode_num: The number of encoders that will be used. Option of just using one of them or both (only input 1 or 2)

        """
        self.power_pin = power
        self.dir_a_pin = dir_a
        self.dir_b_pin = dir_b
        if encode_num != 1 or encode_num != 2:
            print("Not a valid input for the motor encoder number")
            print("Program will not exit")
            exit
        self.encode_num = encode_num

    def forwards():
        """
        Optional parameter to define what forwards is
        """

    def move_cont(direction):
        direction specification is either a or b

    def stop():
        """
        Stops the motor rotation but setting PWM and direction pins to off
        """

    def encoder_pins(encode_a, encode_b=None):
        """
        If using features like the move_distance command. Setup of the encoder pins.

        Args:
            encode_a: Required pin definition for an Encoder output.
            encode_b: Optional pin definintion for extra encoder output.

        """
        if self.encode_num == 2 and encode_b is None:
            # Error case where the encoder pins have not been set correctly.
            print("2 Encoder pins set yet only 1 has been defined. Please define 2 encoder pins or only define one encoder in the pololu_motor class call")
            print("Program will not exit")
            exit

        self.encode_a = encode_a
        
        if self.encode_num == 2:
            self.encode_b = encode_b

    def dis_setup(gear_ratio,wheel_diam,counts_per_rev): #TODO: Finish function
        """
        Function to setup the distance calculation feature of this class for advanced usage.

        Args:
            gear_ratio: This is the gear ratio between the shaft with the encoders (typically the motor shaft) and the final output shaft(one with drive wheels).
            wheel_diam: In meters, this is the diameter of the drive wheels.
            counts_per_rev: The ammount of rises and falls the encoder pulses (both if defined) will have over a singular rotation of the encoder shaft (typically motor shaft).

        """

    def move_dis(direction): #TODO: Finish function
        direction = a or b

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
