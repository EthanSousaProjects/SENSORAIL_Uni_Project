"""
Simple file to test stepper class/ code works as expected.
"""

## Inputs to testing script

# Stepper controllers on our system are as follows:
#   - Controller A: step = 0, dir = 1
#   - Controller B: step = 6, dir 7
stepper_test = False # Test the stepper motor
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
motor_test = True # Test the drive motor
motor_dir_pin_a = 10 # BCM number
motor_dir_pin_b = 11 # BCM number
motor_pwm_pin = 12 # BCM number
motor_power_max = 50 # Between 0 and 100 where 1 is max power and 0 is basically off max power the test will put on the motor
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
    from time import sleep

    # General Setup
    drive_motor = motor.pololu_motor(motor_pwm_pin,motor_dir_pin_a,motor_dir_pin_b)
    print("herea")
    drive_motor.move_cont("a",motor_power_max)
    print("herea")
    sleep(2)
    drive_motor.move_cont("b",motor_power_max)
    print("herea")
    sleep(2)
    drive_motor.duty_cycle_change(motor_power_max/2)
    print("herea")
    sleep(2)
    drive_motor.stop()
    print("herea")
    sleep(1)
    drive_motor.forwards("a")
    drive_motor.move_cont("forward",motor_power_max)
    sleep(2)
    drive_motor.stop()
    sleep(1)
    drive_motor.move_cont("backward", motor_power_max)
    sleep(2)
    drive_motor.stop()
    sleep(2)


if gps_test==True:
    import gps # Import feature package

    longitude, latitude = gps.current_location()

    print("Longitude =",longitude)
    print("latitude =", latitude)