"""
check_input: validator for if input meets the criteria
"""
import random


class RandomNumberList:
    """
    Class for checking input that has several different checkers within it.
    All numbers must be greater than zero.
    """

    def __init__(self, number, pick, put_back=False):
        """ 
        Checks if the given input is valid with the provided criteria:

        Parameter:
        number (int):   The number to be checked
        pick (int):     The number of items to be picked
        put_back (bool): Whether drawn items are to be returned to the sample, 
                        so they can be drawn again (Default = False)
        """

        self.number = number
        self.pick = pick
        self.put_back = put_back

    # @property()
    def return_list(number, pick, put_back=False, error_text=False):
        """
        Will randomly pick the required number of items from a specified sample size.
        Option to place drawn items back in the sample to be drawn again:

        Parameter:
        number (int):   The number of items in the sample pool
        pick (int):     The number of items to be drawn (Default = 1)
        put_back (bool): Whether drawn items are to be returned to the sample, 
                        so they can be drawn again (Default = False)
        error_text(bool): True will print a short error message on the terminal to advise 
                        of why the error occured. Default of False, suppresses error text.

        If an error is encountered it will return False
        """

        # converts the number value to an integer so it can be interogated
        try:
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
        except Exception:
            if error_text:
                Print(
                    f'Invalid parameters have been passed:\nnumber: {number}, pick: {pick}, put_back: {put_back}.')
            return False

    # @property()
    def verify_number(number, error_text=False):
        """
        Will make sure the number passed to MakeDrawVerify is an integer greater than or equal to one.

        Parameter:
        number (int):   The number of items in the sample pool
        error_text(bool): True will print a short error message on the terminal to advise 
                        of why the error occured. Default of False, suppresses error text.

        Returns:
        Boolean
        True:   if number value meets the criteria
        False:  if the criteria is not met

        error_text(bool): True will print a short error message on the terminal to advise 
                        of why the error occured. Default of False, suppresses error text.

        If an error is encountered it will return False


        """
        try:
            if int(number) >= 1:
                return True
            else:
                return False
        except ValueError:
            if error_text:
                print(
                    f"ValueError: number: {number} - number can't be less than zero.")

            return False
        except TypeError:
            if error_text:
                print(f"Error: number: {number} - is not a number.")

            return False
        except Exception:
            if error_text:
                print(
                    f"Error: parameter passed is not valid - number: {number}")
            return false

    # @property()
    def verify_pick(number, pick, error_text=False):
        """
        Will make sure the number and pick quantity passed to MakeDrawVerify are:
        > integers greater than or equal to one;
        > the value of pick is less than the value of number.

        Paremeters:
        number (int):   The number of items in the sample pool
        pick (int):     The number of items to be drawn (Default = 1)
        error_text(bool): True will print a short error message on the terminal to advise 
                        of why the error occured. Default of False, suppresses error text.


        Returns:
        Boolean
        True:   if pick value meets the criteria
        False:  if the criteria is not met

        error_text(bool): True will print a short error message on the terminal to advise 
                        of why the error occured. Default of False, suppresses error text.

        If an error is encountered it will return False

        """
        try:
            if 1 <= int(pick) <= int(number):
                return True
            else:
                return False
        except ValueError:
            if error_text:
                print(
                    f"ValueError: number: {number} & pick: {pick} - must be greater than zero.\nPick: {pick} must be less than or equal to number: {number}")
            return False
        except TypeError:
            if error_text:
                print(
                    f"Error: number: {number} and / or pick: {pick} - are / is not a nuber.")
            return False
        except Exception:
            if error_text:
                print(
                    f"Error: parameters passed are not valid - number: {number}, pick: {pick}")
            return False
