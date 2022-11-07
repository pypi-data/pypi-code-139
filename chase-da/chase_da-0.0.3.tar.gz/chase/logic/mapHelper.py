import logging
import random
import math

from chase.model.sheep import Sheep
from chase.model.wolf import Wolf


def is_coordinate_empty(coX: float, coY: float, sheep_list: list, wolf: Wolf):
    logging.debug("Checking if the coordinates are busy")
    if (coX is wolf.coX) and (coY is wolf.coY):
        logging.warning("the sheep is trying to enter the coordinates of the wolf")
        return False
    for entity in sheep_list:
        if (coX is entity.coX) and (coY is entity.coY) and entity.isAlive:
            logging.info("Coordinates are in use")
            return False
    return True


def calculate_distances(sheep: Sheep, wolf: Wolf):
    sheep.distance = round(math.sqrt((sheep.coX - wolf.coX) ** 2 + (sheep.coY - wolf.coY) ** 2), 3)


def simulate_direction():
    return random.choice("NEWS")


def get_sheep_cords(sheep: Sheep, wolf: Wolf):
    wolf.coX = sheep.coX
    wolf.coY = sheep.coY
