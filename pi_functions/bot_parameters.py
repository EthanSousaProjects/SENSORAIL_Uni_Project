"""
This file contains all of the standard bot parameters like the pin numbers, wheel diameters, leads, etc of the bot.
It is designed to keep everything together so that this file can just be imported and then properties can be used as needed.

When there is > 1 of something a, b, etc is used
    where the closest thing to the pi is the lower letter and the higher letters is as it moves away from pi.

Note that pin numbers are BCM numbers
"""

## Drive motors related properties.

# Properties shared between motors
drive_mots_max_pow = 0.5
drive_mots_freq = 10000

# Mot A
drive_a_pwm_pin = 13
drive_a_dira_pin = 8
drive_a_dirb_pin = 9

#Mot B
drive_b_pwm_pin = 12
drive_b_dira_pin = 10
drive_b_dirb_pin = 11


## Clamping Steppers related properties

clam_step_a_step_pin = 
clam_step_a_dir_pin = 

clam_step_b_step_pin = 
clam_step_b_dir_pin = 
