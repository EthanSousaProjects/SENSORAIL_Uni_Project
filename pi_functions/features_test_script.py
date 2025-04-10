"""
Simple file to test stepper class/ code works as expected.
"""

## Inputs to testing script

stepper_test = True # Test the stepper motor
stepper_dir_pin = 7 # BCM number
stepper_step_pin = 6 # BCM number
stepper_continueos_pulse = False # Will setup an infinite loop to pulse step pin for current limit setup Will always be in True direction
stepper_steps_to_run = 400 # Ammount of steps to run
stepper_up_direction = True # What is considered up (True or False) True is when gpio pin is energised
stepper_lead = 0.002 # Given in meters
stepper_steps_per_rev = 200 # How many full steps per revolution of stepper shaft
stepper_step_size = 1 # Normally 1 for full stepping but 0.5 for half stepping etc.
stepper_dis = 0.01 # Distance to travel given in meters.


# Motor controllers on our system are as follows:
#   - Controller A: pwm = 13, dira = 8, dirb = 9
#   - Controller B: pwm = 12, dira = 10, dirb = 11
motor_test = False # Test the drive motor
motor_dir_pin_a = 10 # BCM number
motor_dir_pin_b = 11 # BCM number
motor_pwm_pin = 12 # BCM number
motor_power_max = 0.5 # Between 0 and 1 where 1 is max power and 0 is basically off max power the test will put on the motor
motor_run_time = 10 # Given in secounds it is the time the motor will be powered on for ech test.
motor_custom_frequency = 10000 # Given in Hz default is currently 1000 Hz.
motor_forwards = "a" # Set the direction pin which is considered forwards.


gps_test = False


## Testing section
if stepper_test == True:
    import stepper # import fearture package

    # General Setup
    stepper_motor = stepper.pololu_stepper(stepper_dir_pin,stepper_step_pin)
    stepper_motor.up(stepper_up_direction)

    if stepper_continueos_pulse == True:
        while True:
            stepper_motor.move_steps(True,100)

    # Running up and down test
    stepper_motor.move_steps(True,stepper_steps_to_run)
    stepper_motor.move_steps(False,stepper_steps_to_run)
    stepper_motor.move_steps("up",stepper_steps_to_run)
    stepper_motor.move_steps("down",stepper_steps_to_run)

    # Advanced feature test
    stepper_motor.dis_setup(stepper_steps_to_run,stepper_lead,stepper_step_size)

    stepper_motor.move_dis(True,stepper_dis)
    stepper_motor.move_dis(False,stepper_dis)
    stepper_motor.move_dis("up",stepper_dis)
    stepper_motor.move_dis("down",stepper_dis)

if motor_test==True:
    import motor # Import feature package


"""
# Bellow is backup code i know works on pi just kept here just incase.

from gpiozero import LED, PWMLED, Button
import time

p = PWMLED(13,frequency=1000)
d = LED(8)
dtwo = LED(9)
d.on()


while (True):
    p.value = 1
    time.sleep(2)
    p.value = 0.5
    time.sleep(2)
    d.off()
    dtwo.on()
    time.sleep(2)
    dtwo.off()
    d.on()





## got steppers to work with the bellow code. adjust this features test script to test these things
from gpiozero import LED
from time import sleep

red = LED(6)
green = LED(7)

green.on()


for i in range(400):
    red.on()
    sleep(0.0015)
    red.off()
    sleep(0.0015)

green.off()

for b in range(400):
    red.on()
    sleep(0.0015)
    red.off()
    sleep(0.0015)
"""