"""
Simple file to test stepper class/ code works as expected.
"""

## Inputs to testing script

stepper_test = True # Test the stepper motor
stepper_dir_pin = 1 # BCM number
stepper_step_pin = 0 # BCM number
stepper_continueos_pulse = True # Will setup an infinite loop to pulse step pin for current limit setup Will always be in True direction
stepper_steps_to_run = 10 # Ammount of steps to run
stepper_up_direction = True # What is considered up (True or False) True is when gpio pin is energised
stepper_lead = 0.002 # Given in meters
stepper_steps_per_rev = 200 # How many full steps per revolution of stepper shaft
stepper_step_size = 1 # Normally 1 for full stepping but 0.5 for half stepping etc.
stepper_dis = 0.01 # Distance to travel given in meters.

motor_test = False

gps_test = False


## Testing section
if stepper_test == True:
    import stepper # import fearture package
    import asyncio

    # General Setup
    stepper_motor = stepper.pololu_stepper(stepper_dir_pin,stepper_step_pin)
    stepper_motor.up(stepper_up_direction)

    if stepper_continueos_pulse == True:
        while True:
            asyncio.run(stepper_motor.move_steps(True,100))

    # Running up and down test
    asyncio.run(stepper_motor.move_steps(True,stepper_steps_to_run))
    asyncio.run(stepper_motor.move_steps(False,stepper_steps_to_run))
    asyncio.run(stepper_motor.move_steps("up",stepper_steps_to_run))
    asyncio.run(stepper_motor.move_steps("down",stepper_steps_to_run))

    # Advanced feature test
    stepper_motor.dis_setup(stepper_steps_to_run,stepper_lead,stepper_step_size)

    stepper_motor.move_dis(True,stepper_dis)
    stepper_motor.move_dis(False,stepper_dis)
    stepper_motor.move_dis("up",stepper_dis)
    stepper_motor.move_dis("down",stepper_dis)