from chase.model.entity import Entity


class Sheep(Entity):

    def __init__(self, id, coX, coY):
        super().__init__(coX, coY)
        self.distance = 0
        self.id = id
        self.isAlive = True

    def __str__(self):
        return "Sheep[id= " + str(self.id) \
               + ", coX= " + str(round(self.coX, 3)) \
               + ", coY= " + str(round(self.coY, 3)) \
               + ", isAlive= " \
               + str(self.isAlive) \
               + "]"
