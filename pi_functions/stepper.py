"""

class to manage things with the stepper motors.

"""

import asyncio

try:
    import RPi.GPIO as gpio
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")
    print("Program will now exit")
    exit

class pololu_stepper:
    """
    A class to manage the plolu stepper motors

    The class with give the user the ability to move a certain number of steps in a specified direction or a specfic distance discrined
    """
    #TODO: write out what the function does and how to use it.
    #TODO: Write out the method to step the stepper motor by one step or multiple based on input
    
    def _init_(dir_pin,step_pin,step_time=0.01):
        """
        Parameters needed to setup the class.

        Pin numbers must be the board numbers not the BCM numbers.

        Args:
            dir_pin: Pin to set rotation of stepper motor on controller
            step_pin: The pin that actives step commands.
            (optional)step_time: This is the time that will be waited after a gpio pin is turned off or turned on for the step commands (in secounds)
        """

        self.dir_pin = dir_pin
        self.step_pin = step_pin

        # GPIO setup
        gpio.setmode(gpio.BOARD)
        gpio.setup(dir_pin,gpio.OUT)
        gpio.setup(dir_pin,gpio.OUT)



    def up(up_dir): #TODO: Finish Function
        """
        Optional parameter to determine which direction is considered up. Easier to write up or down instead of a or b.
        
        Args:
            up_dir: 
        """



    def move_step(): #TODO: Make it so that the stepper rotates when this method is called
        """

        """

    def 

    def move_dis(direction, distance): #TODO: Finish function
    