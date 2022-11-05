import logging

from chase.dao.FileHelper import save_csv, save_json
from chase.factories.sheepFactory import SheepFactory
from chase.logic.mapHelper import calculate_distances
from chase.logic.mapHelper import get_sheep_cords
from chase.logic.mapHelper import is_coordinate_empty
from chase.logic.mapHelper import simulate_direction
from chase.model.sheep import Sheep
from chase.model.wolf import Wolf


class GameSimulation:

    def __init__(self, init_pos_limit, sheep_amount, sheep_move_dist, wolf_move_dist, wait, directory):
        self.init_pos_limit = init_pos_limit
        self.sheep_amount = sheep_amount
        self.sheep_move_dist = sheep_move_dist
        self.wolf_move_dist = wolf_move_dist
        self.wait = wait
        self.directory = directory
        self.sheep_list = list()
        self.wolf = Wolf(0, 0)

    def start_simulation(self, rounds_number):
        self.sheep_list = SheepFactory(self.init_pos_limit).create_sheep(self.sheep_amount)
        for i in range(1, rounds_number + 1):
            if self.wolf.killed_sheep == self.sheep_amount:
                print("All sheep are dead!")
                logging.info("All sheep are dead!")
                break
            print("rounds_number: " + str(i) + "\n" +
                  self.wolf.__str__() +
                  "\nNumber of alive sheep: " + str(self.sheep_amount - self.wolf.killed_sheep))
            logging.info("rounds_number: " + str(i) + "\n" +
                         self.wolf.__str__() +
                         "\nNumber of alive sheep: " + str(self.sheep_amount - self.wolf.killed_sheep))
            logging.debug("rounds_number:" + str(i + 1) + "\n" + self.__str__())
            self.move_alive_sheep()
            [calculate_distances(sheep, self.wolf) for sheep in self.sheep_list if sheep.isAlive]
            self.move_wolf()
            save_csv(i, self.sheep_amount - self.wolf.killed_sheep, self.directory)
            save_json(i, self.sheep_list, self.wolf, self.directory)
            if self.wait:
                input("Press a key to continue!")

    def move_alive_sheep(self):
        [self.change_sheep_coordinates(sheep) for sheep in self.sheep_list]

    def move_wolf(self):
        if not self.is_wolf_able_to_eat():
            nearest_sheep = min([sheep for sheep in self.sheep_list if sheep.isAlive],
                                key=lambda sheep: sheep.distance)
            logging.info("Wolf is chasing sheep ID: " + str(nearest_sheep.id))
            print("Wolf is chasing sheep ID: " + str(nearest_sheep.id))
            self.change_wolf_coordinates(nearest_sheep)

    def change_sheep_coordinates(self, sheep: Sheep):
        if not sheep.isAlive:
            logging.debug("Sheep ID: " + str(sheep.id) + " is dead")
            return
        genX = sheep.coX
        genY = sheep.coY
        match simulate_direction():
            case "N":
                genY += self.sheep_move_dist
            case "S":
                genY -= self.sheep_move_dist
            case "W":
                genX -= self.sheep_move_dist
            case "E":
                genX += self.sheep_move_dist
            case _:
                raise ValueError("the sheep is trying to move in the wrong direction")
        if is_coordinate_empty(genX, genY, self.sheep_list, self.wolf):
            sheep.coX = genX
            sheep.coY = genY
        else:
            logging.debug("The drawn coordinate is busy")
            self.emergency_move(sheep)

    def emergency_move(self, sheep: Sheep):
        genX = sheep.coX
        genY = sheep.coY
        if is_coordinate_empty(genX, genY + self.sheep_move_dist, self.sheep_list, self.wolf):
            logging.debug("managed to change the coordinates to the N")
            sheep.coY = genY + self.sheep_move_dist
            return
        elif is_coordinate_empty(genX, genY - self.sheep_move_dist, self.sheep_list, self.wolf):
            logging.debug("managed to change the coordinates to the S")
            sheep.coY = genY - self.sheep_move_dist
            return
        elif is_coordinate_empty(genX + self.sheep_move_dist, genY, self.sheep_list, self.wolf):
            logging.debug("managed to change the coordinates to the E")
            sheep.coX = genX + self.sheep_move_dist
            return
        elif is_coordinate_empty(genX - self.sheep_move_dist, genY, self.sheep_list, self.wolf):
            logging.debug("managed to change the coordinates to the W")
            sheep.coX = genX - self.sheep_move_dist
            return
        else:
            logging.warning("Cannot move Sheep!, This entity is blocked")

    def change_wolf_coordinates(self, nearest_sheep: Sheep):
        self.wolf.coX += round(
            self.wolf_move_dist * ((nearest_sheep.coX - self.wolf.coX) / nearest_sheep.distance), 3)
        self.wolf.coY += round(
            self.wolf_move_dist * ((nearest_sheep.coY - self.wolf.coY) / nearest_sheep.distance), 3)

    def is_wolf_able_to_eat(self):
        for sheep in self.sheep_list:
            if sheep.distance <= self.wolf_move_dist and sheep.isAlive:
                logging.info("Wolf killed sheep, ID: " + str(sheep.id))
                print("Wolf killed sheep, ID: " + str(sheep.id))
                sheep.isAlive = False
                get_sheep_cords(sheep, self.wolf)
                self.wolf.killed_sheep += 1
                return True
        return False

    def __str__(self):
        result = ""
        for entity in self.sheep_list:
            result = result + entity.__str__() + "\n"
        return "GameSimulation Map Status[\n" + result + self.wolf.__str__() + "]"
