# Imports for controller support
import pygame

# Imoports for bot properties/ features
from bot_parameters import*
import motor
import stepper
from time import sleep

## Bot setup
# Drive motors
drive_mot_a = motor.pololu_motor(drive_a_pwm_pin,drive_a_dira_pin,drive_a_dirb_pin)
drive_mot_b = motor.pololu_motor(drive_b_pwm_pin,drive_b_dira_pin,drive_b_dirb_pin)
drive_mot_b.forwards(drive_b_forwards)
drive_mot_a.forwards(drive_a_forwards)

# Steppers
clam_step_a = stepper.pololu_stepper(clam_step_a_dir_pin,clam_step_a_step_pin)
clam_step_b = stepper.pololu_stepper(clam_step_b_dir_pin,clam_step_b_step_pin)
clam_step_a.up(False)
clam_step_b.up(True)

## TODO: Use this script to manually control the bot using a controller. A first party xbox one is what we have been using.

# Initialize pygame and joystick module
pygame.init()
pygame.joystick.init()

# Check for connected controllers
if pygame.joystick.get_count() == 0:
    print("No Xbox controller detected.")
    pygame.quit()
    exit()

# Initialize the first joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"Connected to: {joystick.get_name()}")

# Define button mappings
BUTTON_A = 0
BUTTON_B = 1
BUTTON_X = 2
BUTTON_Y = 3
BUTTON_LB = 4
BUTTON_RB = 5
BUTTON_BACK = 6
BUTTON_START = 7
BUTTON_LS = 9  # Left stick press
BUTTON_RS = 8  # Right stick press

# Define stick axes
AXIS_LS_X = 0
AXIS_LS_Y = 1
AXIS_RS_X = 3
AXIS_RS_Y = 4
AXIS_LT = 2  # Left trigger
AXIS_RT = 5  # Right trigger

# Define deadzone threshold
DEADZONE = 0.2

# Define functions for button actions
def action_a():
    print("A button pressed - Performing action A")
    drive_mot_b.move_cont("forward",drive_mots_max_pow)
    drive_mot_a.move_cont("forward",drive_mots_max_pow)
    sleep(1)
    drive_mot_b.stop()
    drive_mot_a.stop()


def action_b():
    print("B button pressed - Performing action B")
    drive_mot_b.move_cont("backward",drive_mots_max_pow)
    drive_mot_a.move_cont("backward",drive_mots_max_pow)
    sleep(1)
    drive_mot_b.stop()
    drive_mot_a.stop()

def action_x():
    print("X button pressed - Performing action X")
    clam_step_b.move_steps("down",Clamp_max_steps)
    clam_step_a.move_steps("down",Clamp_max_steps)


def action_y():
    print("Y button pressed - Performing action Y")
    clam_step_b.move_steps("up",Clamp_max_steps)
    clam_step_a.move_steps("up",Clamp_max_steps)

def action_lb():
    print("Left Bumper pressed - Performing action LB")

def action_rb():
    print("Right Bumper pressed - Performing action RB")

def action_back():
    print("Back button pressed - Performing action Back")

def action_start():
    print("Start button pressed - Performing action Start")

def action_ls():
    print("Left Stick pressed - Performing action LS")

def action_rs():
    print("Right Stick pressed - Performing action RS")

def handle_stick_movement():
    ls_x = joystick.get_axis(AXIS_LS_X)
    ls_y = joystick.get_axis(AXIS_LS_Y)
    rs_x = joystick.get_axis(AXIS_RS_X)
    rs_y = joystick.get_axis(AXIS_RS_Y)
    
    if abs(ls_x) > DEADZONE or abs(ls_y) > DEADZONE:
        print(f"Left Stick: ({ls_x:.2f}, {ls_y:.2f})")
    if abs(rs_x) > DEADZONE or abs(rs_y) > DEADZONE:
        print(f"Right Stick: ({rs_x:.2f}, {rs_y:.2f})")

def handle_triggers():
    lt = joystick.get_axis(AXIS_LT)
    rt = joystick.get_axis(AXIS_RT)
    print(f"Left Trigger: {lt:.2f} | Right Trigger: {rt:.2f}")
    #if rt > 0:

# Mapping of buttons to functions
button_actions = {
    BUTTON_A: action_a,
    BUTTON_B: action_b,
    BUTTON_X: action_x,
    BUTTON_Y: action_y,
    BUTTON_LB: action_lb,
    BUTTON_RB: action_rb,
    BUTTON_BACK: action_back,
    BUTTON_START: action_start,
    BUTTON_LS: action_ls,
    BUTTON_RS: action_rs,
}

# Main loop
running = True
print("Listening for controller input... Press START to exit.")
while running:
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            button = event.button
            if button in button_actions:
                button_actions[button]()
                
            # Exit if START button is pressed
            if button == BUTTON_START:
                running = False
        
    # Handle stick movement and triggers
    handle_stick_movement()
    handle_triggers()

pygame.quit()
print("Controller input listener exited.")
