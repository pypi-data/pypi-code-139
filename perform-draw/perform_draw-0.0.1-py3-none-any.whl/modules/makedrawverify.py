"""
check_input: validator for if input meets the criteria
"""


class MakeDrawVerify:
    """
    Class for checking input that has several different checkers within it.
    All numbers must be greater than zero.
    """

    def __init__(self, number, pick):
        """ 
        Checks if the given input is valid with the provided criteria:

        Parameter:
        number (int): The number to be checked
        pick (int): the number of items to be picked
        """

        self.number = number
        self.pick = pick

    @property
    def verify_number(self):
        """
        Will make sure the number passed to MakeDrawVerify is an integer greater than or equal to one.

        Paremeters:
        None as it uses the number value from the MakeDrawVerify object.

        Returns:
        Boolean
        True:   if number value meets the criteria
        False:  if the criteria is not met
        """
        try:
            if int(self.number) >= 1:
                self.__verify_number = True
                return True
            else:
                return False
        except ValueError:
            print(
                f"ValueError: number: {self.number} - number can't be less than zero.")
            return False
        except TypeError:
            print(f"Error: number: {self.number} - is not a number.")
            return False
        else:
            print(
                f"Error: parameter passed is not valid - number: {self.number}")
            return false

    @property
    def verify_pick(self):
        """
        Will make sure the number and pick quantity passed to MakeDrawVerify are:
        > integers greater than or equal to one;
        > the value of pick is less than the value of number.

        Paremeters:
        None as it uses the number and pick values from the MakeDrawVerify object.

        Returns:
        Boolean
        True:   if pick value meets the criteria
        False:  if the criteria is not met
        """
        try:
            if 1 <= int(self.pick) <= int(self.number):
                self.__verify_pick = True
                return True
            else:
                return False
        except ValueError:
            print(
                f"ValueError: number: {self.number} & pick: {self.pick} - must be greater than zero.\nPick: {self.pick} must be less than or equal to number: {self.number}")
            self.__verify_pick = False
            return False
        except TypeError:
            print(
                f"Error: number: {self.number} and / or pick: {self.pick} - are / is not a nuber.")
            return False
        else:
            print(
                f"Error: parameters passed are not valid - number: {self.number}, pick: {self.pick}")
            return False
