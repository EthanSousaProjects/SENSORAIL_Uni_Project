"""

Class to manage things with a motor and the encoder outputs.

Defines distance traveled and and on and off function for manual movements.
"""

from sys import exit
from math import pi
import asyncio

try:
    import RPi.GPIO as gpio
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")
    print("Program will not exit")
    exit

#TODO: Finish making this motor class See description on what has to be made.
#TODO: double check all comments/ doc strings are formatted + described correctly.
#TODO: Test class works as i expect.
class pololu_motor:
    """
    A class to manage the pololu motors and their encoders.
    The basic class setup will contain functions to set the motors power and rotation direction (A or B)

    The advanced setup will move the bot a set distance based on setup parameters. Run <object name>.encode_pins and <object name>.dis_setup to finished advanced setup.

    Pins numbers must be the board numbers not the BCM numbers.

    Args:
        power_pin: the pwm pin that sets the power of the motor
        dir_a: The gpio pin which defines if the motor will rotate in the A direction (clockwise/ anti) opposite to B direction
        dir_b: The gpio pin which defines if the motor will rotate in the B direction (clockwise/ anti) opposite to A direction
        (optional)encode_num: The number of encoders that will be used. Option of just using one of them or both (only input 1 or 2). Default is None. 
        (optional)pwm_freq: The frequency of which the pwm signal will run at Default is 1000.
    """
    #TODO: Finish off writing the comment above so that the usage of the class is clear.
    def _init_(power_pin,dir_a,dir_b,encode_num=None,pwm_freq=1000):
        """
        Parameters needed when setting up the class

        Pins numbers must be the board numbers not the BCM numbers.

        Args:
            power_pin: the pwm pin that sets the power of the motor
            dir_a: The gpio pin which defines if the motor will rotate in the A direction (clockwise/ anti) opposite to B direction
            dir_b: The gpio pin which defines if the motor will rotate in the B direction (clockwise/ anti) opposite to A direction
            (optional)encode_num: The number of encoders that will be used. Option of just using one of them or both (only input 1 or 2). Default is None. 
            (optional)pwm_freq: The frequency of which the pwm signal will run at Default is 1000.
        """
        # Input error checks
        if encode_num != 1 and encode_num != 2 and encode_num is not None:
            print("Not a valid input for the motor encoder number")
            print("Program will not exit")
            exit
        elif power_pin < 1 or power_pin > 40 or type(power_pin) is not int:
            print("power pin incorrectly defined. Either not between 1 and 40 or not an integer")
            print("Program will not exit")
            exit
        elif dir_a < 1 or dir_a > 40 or type(dir_a) is not int:
            print("Direction a pin incorrectly defined. Either not between 1 and 40 or not an integer")
            print("Program will not exit")
            exit
        elif dir_b < 1 or dir_b > 40 or type(dir_b) is not int:
            print("Direction b pin incorrectly defined. Either not between 1 and 40 or not an integer")
            print("Program will not exit")
            exit

        # Setting class variables to use in later methods
        self.dir_a = dir_a
        self.dir_b = dir_b
        self.encode_num = encode_num
        self.forwards_dir = None

        gpio.setmode(gpio.BOARD) # Setting up gpio pins to be numbered based on the board number and not the BCM number
        # pwm setup
        self.power = gpio.PWM(power_pin,pwm_freq)
        # Direction setup
        gpio.setup(dir_a, gpio.OUT)
        gpio.setup(dir_b, gpio.OUT)

    def forwards(forwards_dir):
        """
        Optional parameter to define what forwards is. Makes it easier to say move forwards or backwards.

        Args:
            forwards_dir: The direction (a or b/ clockwise or anticlockwise) that coresponds to a forward movement of the bot. Must be a or b as a string.
        """
        if forwards_dir == "a" or forwards_dir == "b":
            self.forwards_dir = forwards_dir
        else:
            print("Forwards direction of motor inproperly defined.")
            print("Program will not exit")
            exit

    def move_cont(direction, duty):
        """
        Turn the motor on until program stops or the motor is told to stop.

        Args:
            direction(string): Can be either 'a' or 'b' be default. If the forwards setup method has been used then 'forward' and 'backward' are valid parameters.
            duty(float): The Duty cycle of the pwm signal. 0.0 is no power 100.0 is full power. In a percent.
        """
        
        # Direction enable + error check
        if direction != "a" and direction != "b" and direction != "forward" and direction != "backward":
            print("Motor moving direction has not been specified correctly. Plases specifiy a valid direction input.")
            print("Program will not exit")
            exit
        
        elif duty < 0.0 or duty > 100.0:
            print("Motor power pwm duty cycle is set to high. Value must be between 0 and 100")
            print("Program will not exit")
            exit
          
        elif direction == "a":
            gpio.output(self.dir_a,True)

        elif direction == "b":
            gpio.output(self.dir_b,True)

        elif direction == "foward" or direction == "backward" and self.forwards_dir is None:
            print("Motor specificed to move forwards or backwards but, forwards direction has not been set.")
            print("Please specifiy a forwards direction before using forwards or backwards.")
            print("Program will not exit")
            exit
        
        elif direction == "forwards":
            if self.forwards_dir == "a":
                gpio.output(self.dir_a, True)
            
            else:
                gpio.output(self.dir_b, True)

        else:
            # Direction is known to be backwards so just oposite of forward direction
            if self.forwards_dir == "a":
                gpio.output(self.dir_b, True)
            
            else:
                gpio.output(self.dir_a, True)

        # PWM/ power enable
        if duty < 0.0 or duty > 100.0:
            print("Motor power pwm duty cycle is set to high. Value must be between 0 and 100")
            print("Program will not exit")
            exit
        
        self.power.start(duty)

    def stop():
        """
        Stops the motor rotation by setting PWM and direction pins to off/ low.
        """
        self.power.stop()
        gpio.output(self.dir_a,False)
        gpio.output(self.dir_b,False)
        

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
        elif self.encode_num is None:
            print("The encoder pins have not been setup on the class initialization")
            print("Program will not exit")
            exit

        self.encode_a = encode_a
        gpio.setup(encode_a, gpio.IN, pull_up_down=gpio.PUD_UP)
        
        if self.encode_num == 2:
            self.encode_b = encode_b
            gpio.setup(encode_b, gpio.IN, pull_up_down=gpio.PUD_UP)

    def dis_setup(gear_ratio,wheel_diam,counts_per_rev):
        """
        Function to setup the distance calculation feature of this class for advanced usage.

        Args:
            gear_ratio: This is the gear ratio between the shaft with the encoders (typically the motor shaft) and the final output shaft(one with drive wheels). Code takes this gear ratio as 1 rotation of encoder shaft to ammount of rotation of final output shaft. Reduction ratio < 1 increaser ratio > 1.
            wheel_diam: In meters, this is the diameter of the drive wheels.
            counts_per_rev: The ammount of rises and falls the encoder pulses (both if defined) will have over a singular rotation of the encoder shaft (typically motor shaft).
        """
        if gear_ratio <= 0.0 or wheel_diam <= 0.0 or counts_per_rev <= 0.0:
            print("Incorrect definition or gear ratio, wheel diameter or counts per revolution. Please define correctly.")
            print("Program will not exit")
            exit
        
        self.gear_ratio = gear_ratio
        self.wheel_circum = wheel_diam * pi
        self.counts_per_rev = counts_per_rev

    def encode_pulse_count():
        self.counted_pulses += 1

    
    async def move_dis(direction, duty, distance): #TODO: Finish function
        """
        Turn the motor on until you have gone past a certain distance.

        Args:
            direction(string): Can be either 'a' or 'b' be default. If the forwards setup method has been used then 'forward' and 'backward' are valid parameters.
            duty(float): The Duty cycle of the pwm signal. 0.0 is no power 100.0 is full power. In a percent. Is max power the motor will have.
            distance: The target distance to travel of the bot given in meters
        """
        # Error check
        if distance <= 0.0:
            print("Distance to travel ammount is less than or equal to zero. Set direction in the method call and use a positive value in distance parameter")

        # Calculating how many pulses we need to move the required distance.
        needed_Pulses = (distance * self.counts_per_rev)/(self.wheel_circum * self.gear_ratio)

        # gpio and counting setup
        self.counted_pulses = 0
        gpio.add_event_detect(self.encode_a, gpio.BOTH, callback=self.encode_pulse_count)
        if self.encode_num == 2:
            gpio.add_event_detect(self.encode_b, gpio.BOTH, callback=self.encode_pulse_count)

        # Turning motor on
        self.move_cont(direction,duty)

        # Waiting to reach ammount of pulses
        while self.counted_pulses < needed_Pulses:
            await asyncio.sleep(0.0001)
            #TODO: Adjust duty cycle based on how close we are to making distance so that when motor is turned off we are not over shooting due to too much power.

        #Turning motor off
        self.stop()

        #TODO: add in this check of distance moved
        # Checking distance moved prediction is right.

        # Looping untill in 10% error distance?

        # Disabiling gpio encoder counting
        gpio.remove_event_detect(self.encode_a)
        if self.encode_num == 2:
            gpio.remove_event_detect(self.encode_b)
        


gpio.setmode(gpio.BOARD) # use this one as i
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
