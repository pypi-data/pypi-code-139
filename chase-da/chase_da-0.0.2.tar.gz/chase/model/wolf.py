from chase.model.entity import Entity


class Wolf(Entity):

    def __init__(self, coX, coY):
        super().__init__(coX, coY)
        self.killed_sheep = 0

    def __str__(self):
        return "Wolf[" \
               + "coX= " + str(round(self.coX, 3)) \
               + ", coY= " + str(round(self.coY, 3)) \
               + ", kills= " + str(self.killed_sheep) \
               + "]"
