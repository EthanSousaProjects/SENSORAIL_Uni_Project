"""

Class to manage things with a motor and the encoder outputs.

Defines distance traveled and and on and off function for manual movements.

"""

from sys import exit
from math import pi
import asyncio
from gpiozero import LED, PWMLED, Button
# led is for turning on and off gpio pins, pwmled is for pwm signals, button is for inputs to the gpio pins.

#TODO: Account for the distance moving method that there are 2 motors not just 1. Separate from class i think. then pass motors into separate function using same code.
#TODO: Test class works as i expect.
class pololu_motor:
    """
    A class to manage the pololu motors and their encoders.
    The basic class setup will contain functions to set the motors power and rotation direction (A or B)

    The advanced setup will move the bot a set distance based on setup parameters. Run <object name>.encode_pins and <object name>.dis_setup to finished advanced setup.

    Pins numbers must be the BCM numbers.

    Args:
        power_pin: the pwm pin that sets the power of the motor
        dir_a: The gpio pin which defines if the motor will rotate in the A direction (clockwise/ anti) opposite to B direction
        dir_b: The gpio pin which defines if the motor will rotate in the B direction (clockwise/ anti) opposite to A direction
        (optional)encode_num: The number of encoders that will be used. Option of just using one of them or both (only input 1 or 2). Default is None. 
        (optional)pwm_freq: The frequency of which the pwm signal will run at Default is 1000.
    """
    def __init__(self,power_pin,dir_a,dir_b,encode_num=None,pwm_freq=1000):
        """
        Parameters needed when setting up the class

        Pins numbers must be the BCM numbers.

        Args:
            power_pin: the pwm pin that sets the power of the motor
            dir_a: The gpio pin which defines if the motor will rotate in the A direction (clockwise/ anti) opposite to B direction
            dir_b: The gpio pin which defines if the motor will rotate in the B direction (clockwise/ anti) opposite to A direction
            (optional)encode_num: The number of encoders that will be used. Option of just using one of them or both (only input 1 or 2). Default is None. 
            (optional)pwm_freq: The frequency of which the pwm signal will run at Default is 1000 (must be integer).
        """
        # Input error checks
        if encode_num != 1 and encode_num != 2 and encode_num is not None:
            print("Not a valid input for the motor encoder number")
            print("Program will now exit")
            exit
        elif power_pin < 1 or power_pin > 40 or type(power_pin) is not int:
            print("power pin incorrectly defined. Either not between 1 and 40 or not an integer")
            print("Program will now exit")
            exit
        elif dir_a < 1 or dir_a > 40 or type(dir_a) is not int:
            print("Direction a pin incorrectly defined. Either not between 1 and 40 or not an integer")
            print("Program will now exit")
            exit
        elif dir_b < 1 or dir_b > 40 or type(dir_b) is not int:
            print("Direction b pin incorrectly defined. Either not between 1 and 40 or not an integer")
            print("Program will now exit")
            exit
        elif type(pwm_freq) != int:
            print("pwm freqency specified is not an integer. Integer number required")
            print("Program will now exit")
            exit      

        # Setup
        self.dir_a = LED(dir_a)
        self.dir_b = LED(dir_b)
        self.power = PWMLED(power_pin,frequency=pwm_freq)
        self.encode_num = encode_num
        self.forwards_dir = None

    def forwards(self,forwards_dir):
        """
        Optional parameter to define what forwards is. Makes it easier to say move forwards or backwards.

        Args:
            forwards_dir: The direction (a or b) that coresponds to a forward movement of the bot. Must be a or b as a string.
        """
        if forwards_dir == "a" or forwards_dir == "b":
            self.forwards_dir = forwards_dir
        else:
            print("Forwards direction of motor inproperly defined.")
            print("Program will now exit")
            exit

    def move_cont(self,dir, duty):
        """
        Turn the motor on until program stops or the motor is told to stop.

        Args:
            dir(string): Can be either 'a' or 'b' be default. If the forwards setup method has been used then 'forward' and 'backward' are valid parameters.
            duty(float): The Duty cycle of the pwm signal. 0.0 is no power 100.0 is full power. In a percent.
        """
        
        # Direction enable + error check
        if dir != "a" and dir != "b" and dir != "forward" and dir != "backward":
            print("Motor moving direction has not been specified correctly. Plases specifiy a valid direction input.")
            print("Program will now exit")
            exit
        
        elif duty < 0.0 or duty > 100.0:
            print("Motor power pwm duty cycle is set to high. Value must be between 0 and 100")
            print("Program will now exit")
            exit
          
        elif dir == "a":
            self.dir_a.on()

        elif dir == "b":
            self.dir_b.on()

        elif dir == "foward" or dir == "backward" and self.forwards_dir is None:
            print("Motor specificed to move forwards or backwards but, forwards direction has not been set.")
            print("Please specifiy a forwards direction before using forwards or backwards.")
            print("Program will now exit")
            exit
        
        elif dir == "forwards":
            if self.forwards_dir == "a":
                self.dir_a.on()
            
            else:
                self.dir_b.on()

        else:
            # Direction is known to be backwards so just oposite of forward direction
            if self.forwards_dir == "a":
                self.dir_b.on()
            
            else:
                self.dir_a.on()

        # PWM/ power enable
        if duty < 0.0 or duty > 100.0:
            print("Motor power pwm duty cycle is set to high or too low. Value must be between 0 and 100")
            print("Program will now exit")
            exit
        
        self.power.value = duty/100

    def duty_cycle_change(self,duty):
        """
        Change the pwm duty cycle of the motor

        Args:
            duty(float): The Duty cycle of the pwm signal. 0.0 is no power 100.0 is full power. In a percent.
        """
        if duty < 0.0 or duty > 100.0:
            print("Motor power pwm duty cycle is set to high or too low. Value must be between 0 and 100")
            print("Program will now exit")
            exit

        self.power.value = duty/100

    def stop(self):
        """
        Stops the motor rotation by setting PWM and direction pins to off/ low.
        """
        self.power.value = 0
        self.dir_a.off()
        self.dir_b.off()
        
    def encoder_pins(self,encode_a, encode_b=None):
        """
        If using features like the move_distance command. Setup of the encoder pins.

        Must use BCM pin definitions

        Args:
            encode_a: Required pin definition for an Encoder output.
            encode_b: Optional pin definintion for extra encoder output.
        """
        if self.encode_num == 2 and encode_b is None:
            # Error case where the encoder pins have not been set correctly.
            print("2 Encoder pins set yet only 1 has been defined. Please define 2 encoder pins or only define one encoder in the pololu_motor class call")
            print("Program will now exit")
            exit
        elif self.encode_num is None:
            print("The encoder pins have not been setup on the class initialization")
            print("Program will now exit")
            exit

        self.encode_a = Button(encode_a)
        
        if self.encode_num == 2:
            self.encode_b = Button(encode_b)

    def dis_setup(self,gear_ratio,wheel_diam,counts_per_rev):
        """
        Function to setup the distance calculation feature of this class for advanced usage.

        Args:
            gear_ratio: This is the gear ratio between the shaft with the encoders (typically the motor shaft) and the final output shaft(one with drive wheels). Code takes this gear ratio as 1 rotation of encoder shaft to ammount of rotation of final output shaft. Reduction ratio < 1 increaser ratio > 1.
            wheel_diam: In meters, this is the diameter of the drive wheels.
            counts_per_rev: The ammount of rises and falls the encoder pulses (both if defined) will have over a singular rotation of the encoder shaft (typically motor shaft).
        """
        if gear_ratio <= 0.0 or wheel_diam <= 0.0 or counts_per_rev <= 0.0:
            print("Incorrect definition or gear ratio, wheel diameter or counts per revolution. Please define correctly.")
            print("Program will now exit")
            exit
        
        self.gear_ratio = gear_ratio
        self.wheel_circum = wheel_diam * pi
        self.counts_per_rev = counts_per_rev



def encode_pulse_count():
    self.counted_pulses += 1

# Non motor specific function but important to the motors.

async def move_dis(self,dir, duty, distance):
    """
    Turn the motor on until you have gone past a certain distance.

    Must run this method using the 'asyncio.run()' command. Instead of a normall class method call due to the use of async to avoid program from haulting.
    Example is async.run(<classname>.move_dis(a,b,c))

    Args:
        dir(string): Can be either 'a' or 'b' be default. If the forwards setup method has been used then 'forward' and 'backward' are valid parameters.
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

    self.encode_a.when_pressed = encode_pulse_count
    self.encode_a.when_pressed = encode_pulse_count

    if self.encode_num == 2:
        self.encode_b.when_pressed = encode_pulse_count
        self.encode_b.when_pressed = encode_pulse_count

    # Turning motor on
    self.move_cont(dir,duty)

    # Waiting to reach ammount of pulses
    while self.counted_pulses < needed_Pulses:
        await asyncio.sleep(0.0001)

    # Turning motor off
    self.stop()





def mov_dis_two_mot(motor_a, motor_b):
    """
    Turn the motor on until you have gone past a certain distance.

    """