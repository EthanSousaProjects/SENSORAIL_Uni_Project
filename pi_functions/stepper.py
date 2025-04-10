"""

Class to manage things with the pololu stepper motors.

"""

from sys import exit
from math import ceil # Used to round up
from time import sleep
from gpiozero import LED
# led is for turning on and off gpio pins.

class pololu_stepper:
    """
    A class to manage the plolu stepper motors

    The class will give the user the ability to move a certain number of steps in a specified direction or a specfic distance discrined

    Pin numbers must be BCM numbers.
    Args:
        dir_pin: Pin to set rotation of stepper motor on controller
        step_pin: The pin that actives step commands.
        (optional)step_time: This is the time that will be waited after a gpio pin is turned on or off for the step commands (in secounds)
    """
    #TODO:Test on Pi
    def __init__(self,dir_pin,step_pin,step_time=0.015):
        """
        Parameters needed to setup the class.

        Pin numbers must be the BCM numbers.

        Args:
            dir_pin: Pin to set rotation of stepper motor on controller
            step_pin: The pin that actives step commands.
            (optional)step_time: This is the time that will be waited after a gpio pin is turned on or off for the step commands (in secounds) (fastest tested is 0.015s)
        """

        # Setup
        self.dir = LED(dir_pin)
        self.step = LED(step_pin)
        self.up_dir = None
        self.step_time = step_time

    def up(self,up_dir):
        """
        Optional parameter to determine which direction is considered up. Easier to write up or down instead of True or False
        
        Args:
            up_dir: Boolean True or False. True is when direction GPIO pin is energised.
        """

        if up_dir != True and up_dir != False:
            print("Input variable is not a boolean True or False. Please use onlu boolean True or False")
            print("Program will now exit")
            exit
            
        self.up_dir = up_dir

    def move_steps(self,dir,steps):
        """
        Rotate the stepper motor a specifed number of steps in a specified direction.

        Args:
            dir: Direction definition can be `True` or `False` by default. If up method has been used then `up` and `down` are valid parameters.
            steps: the ammount of steps that will be made by the stepper motor (must be whole number of steps If half/ quater stepping is required manually set it up on the control board)
        """

        #Error Check
        if dir == "up" or dir == "down" and self.up_dir == None:
            print("up direction has not been described. Please use True or False or define the up direction using self.up() method")
            print("Program will now exit")
            exit

        elif dir != "up" and dir != "down" and dir != True and dir != False:
            print("Invalid input for direction parameter. Use: up, down, True or False")
            print("Program will now exit")
            exit

        elif steps <= 0 or type(steps) != int:
            print("Invalid step count or steps defined is not an integer.")
            print("Program will now exit")
            exit

        # Setting up direction on stepper control board
        if dir == "up":
            if self.up_dir == True:
                self.dir.on()

            else:
                self.dir.off()
            
        elif dir == "down":
            if self.up_dir != True:
                self.dir.on()
                
            else:
                self.dir.off()

        elif dir == True:
            self.dir.on()

        else:
            # Direction must be False therefore direction pin should be set to off
            self.dir.off()

        # Stepping by creating step signals
        for i in range(steps):
            self.step.on()
            sleep(self.step_time)
            self.step.off()
            sleep(self.step_time)

    def dis_setup(self,steps_per_rev,lead,step_size=1):
        """
        Area to setup the parameters for the move distance feature of the class.

        Args:
            steps_per_rev: The ammount of full steps that are taken for 1 revolution of the lead screw nut.
            lead: The linear travel the nut makes per one screw revolution (given in meters)
            step_size(optional): Step size being used with the stepper motor (normally full step).
        """

        # Parameter error check
        if type(steps_per_rev) != int:
            print("Steps per rev must be an integer")

        elif lead <= 0.0:
            print("Lead number is less than or equal to zero")

        self.dis_per_step = lead / (steps_per_rev * step_size)

    def move_dis(self,dir, dis):
        """
        Method to move a lead screw directly attached to the stepper motor a specifed distance. Not it will round up to nearest step size (normally nearest full step).

        Must have run the method dis_setup to make this work.

        Args:
            dir: Direction definition can be `True` or `False` by default. If up method has been used then `up` and `down` are valid parameters.
            dis: The target distance to get the nut on the lead screw to move (given in meters).
        """
        # Error check
        if dis <= 0:
            print("Distance is less than or equal to zero. Distance must be a positive float")
            print("Program will now exit")
            exit
        # dir error check is done in move steps method so not included here.

        # Calculate how many steps to move
        cal_steps = ceil(dis/self.dis_per_step)

        # Running steps
        self.move_steps(dir, cal_steps)
