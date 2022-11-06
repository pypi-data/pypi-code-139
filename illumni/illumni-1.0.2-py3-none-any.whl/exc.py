class NoRoutesDir(Exception):
    def __init__(self):
        self.message = "The \"routes\" directory does not exist."
        super().__init__(self.message)

class RouteError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class FileNonexistant(Exception):
    def __init__(self):
        self.message = "The file referenced does not exist."
        super().__init__(self.message)