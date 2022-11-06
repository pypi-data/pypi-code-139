import logging
import random

from chase.logic.mapHelper import is_coordinate_empty
from chase.model.sheep import Sheep
from chase.model.wolf import Wolf


class SheepFactory:

    def __init__(self, init_pos_limit):
        self.init_pos_limit = init_pos_limit

    def create_sheep(self, number):
        sheepList = list()
        while len(sheepList) < int(number):
            generatedX = self.draw_value()
            generatedY = self.draw_value()
            if is_coordinate_empty(generatedX, generatedY, sheepList, Wolf(0, 0)):
                sheepList.append(Sheep(len(sheepList) + 1, generatedX, generatedY))
        logging.debug("creating sheep in the amount of: " + str(number))
        return sheepList

    def draw_value(self):
        return round(float(random.uniform(-self.init_pos_limit, self.init_pos_limit)), 3)
