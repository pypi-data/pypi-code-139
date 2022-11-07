"""
make_draw simple function to draw a user defined number of balls from a user defined number of balls available
"""
import math
import random

# these modules are defined within the app
from modules.makedrawverify import MakeDrawVerify
from modules.selector import draw_numbers

# Text for use in the user input requests
number_text = """
Please enter the total number of balls to be placed in the bag:
You must enter a whole number (integer) greater than 0
"""

pick_text = """ 
Please enter the total number of balls to be drawn:
You must enter a whole number (integer) greater than 0
and less than"""


# Ask the user for the number of items in the pool.
number = input(number_text)

# check_number: variable to check if the number value entered by the user is valid
check_number = MakeDrawVerify(number, 1)

if check_number.verify_number:
    # Ask the user for the number of items to be drwn from the pool.
    pick = input(f'{pick_text} {number}.\n')

    # check_pick: variable to check if the pick value entered by the user is valid
    check_pick = MakeDrawVerify(number, pick)

    if check_pick.verify_pick:
        # final verification before the draw
        draw = MakeDrawVerify(number, pick)

        if draw.verify_number and draw.verify_pick:
            put_back = False  # Not defined the input field for this yet

            # calling the draw_numbers object will start the draw and return a list of drawn numbers
            drawn = draw_numbers(number=number, pick=pick, put_back=False)

            print(f'\nNumbers drawn are: {drawn}\n')

        else:
            print(
                f'Please enter valid parameters. You entered:\n    number: {number}\n    pick: {pick}\n')
    else:
        print(f'You entered an inavlid parameter for pick: {pick}.')
else:
    print(f'You entered an invalid parameter for number: {number}.')
