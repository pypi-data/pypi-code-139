import random
import math

from chase.model.sheep import Sheep
from chase.model.wolf import Wolf


def is_coordinate_empty(coX: float, coY: float, sheep_list: list, wolf: Wolf):
    if (coX is wolf.coX) and (coY is wolf.coY):
        return False
    for entity in sheep_list:
        if (coX is entity.coX) and (coY is entity.coY) and entity.isAlive:
            return False
    return True


def calculate_distances(sheep: Sheep, wolf: Wolf):
    sheep.distance = round(math.sqrt((sheep.coX - wolf.coX) ** 2 + (sheep.coY - wolf.coY) ** 2), 3)


def simulate_direction():
    return random.choice("NEWS")


def get_sheep_cords(sheep: Sheep, wolf: Wolf):
    wolf.coX = sheep.coX
    wolf.coY = sheep.coY
