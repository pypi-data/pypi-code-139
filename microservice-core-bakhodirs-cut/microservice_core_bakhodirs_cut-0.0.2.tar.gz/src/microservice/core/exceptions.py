class ValidationException(Exception):
    __slots__ = ["detail"]

    def __init__(self, detail=None):
        self.detail = detail

    def __str__(self):
        return self.detail
