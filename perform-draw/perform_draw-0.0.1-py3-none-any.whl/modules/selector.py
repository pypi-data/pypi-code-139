import math
import random


def draw_numbers(number, pick, put_back):
    """
    Will randomly pick the required number of items from a specified sample size.
    Option to place drawn items back in the sample to be drawn again:

    Parameter:
    number (int):   The number of items in the sample pool
    pick (int):     The number of items to be drawn (Default = 1)
    put_back (bool): Whether drawn items are to be returned to the sample, 
                    so they can be drawn again (Default = False)

    """
    # number: int The total number of balls available to pick from
    # pick:   int The number of balls to pick out the bag ((Default = 1)
    # put_back: Boolean Whether the drawn ball is put back in the bag?, (Default = False)

    # converts the number value to an integer so it can be interogated
    numbers = int(number)
    # converts the pick value to an integer so it can be interogated
    to_pick = int(pick)

    # pool: a list of numbers from 1 to the number value
    pool = list(range(1, numbers + 1))
    # drawn: an empty list that will have the drawn numbers appended to it.
    drawn = []

    # picked: a for loop to draw the numbers and append to the drawn list.
    for picked in range(to_pick):
        index = random.randint(0, numbers - 1)

        item = pool[index]

        drawn.append(item)

        # Checks if the number is to put put back ornot, prior to the next drawn
        if put_back != True:
            pool.pop(index)
            numbers -= 1

    # drawn: the list of the numbers drawn in line with the parameters provided.
    return drawn
