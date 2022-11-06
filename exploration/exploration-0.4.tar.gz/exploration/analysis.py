"""
- Authors: Peter Mawhorter
- Consulted:
- Date: 2022-10-24
- Purpose: Analysis functions for decision graphs an explorations.
"""

from . import core, journal


def describeProgress(exploration: core.Exploration) -> str:
    """
    Describes the progress of an exploration by noting each room/zone
    visited and explaining the options visible at each point plus which
    option was taken. Notes powers/tokens gained/lost along the way.

    Example:
    >>> import pytest
    >>> pytest.xfail("Not implemented yet.")
    >>> e = journal.convertJournal('''\\
    ... S pit Start
    ... A gain jump
    ... A gain attack
    ... n button check
    ... zz Wilds
    ... o up
    ...   q _flight
    ... o left
    ... x left left_nook right
    ... a geo_rock
    ...   At gain geo*15
    ...   At deactivate
    ... o up
    ...   q _tall_narrow
    ... t right
    ... o right
    ...   q attack
    ... x right alcove
    ... u pit
    ... n a few more doors in this area
    ... a kill_bugs
    ...   At gain geo*4
    ... x right_tunnel firefly_platforms bottom_left Climbing_Platforms
    ... a kill_enemies
    ...   At gain geo*2
    ... a geo_rock
    ...   At gain geo*15
    ...   At deactivate
    ... x climb_platforms mid_platforms bottom_right
    ...   q jump
    ... a get_spiked  # oops
    ... ''')
    >>> for line in describeProgress(e).splitlines():
    ...    print(line)
    Start of the exploration
    You are in the zone Start
    You are at the pit
    You gain the power 'jump
    TODO: Fill in what should go here based on the journal above. Feel
    free to change the wording above if there's alternate phrasing you
    like better.
    """
    # TODO: write code here to make the example above come true.
    # You will want to make use of a loop that runs through the
    # different steps of the exploration object (the len function will
    # tell you how many steps it has).
    # You will need to access the current graph (or maybe also the
    # current game state) through the situationAtStep (or maybe also
    # stateAtStep) method, and the positionAtStep and transitionAtStep
    # methods will also come in handy. In fact, the situationAtStep
    # method combines those so it may be more convenient.
    # If you want a challenge, try to use type annotations so that the
    # Thonny assistant shows no errors, but don't worry about the
    # assistant if that's too complicated.
