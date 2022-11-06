from dataclasses import dataclass


@dataclass
class NuzlockeState:
    game: str
    progress: int
    pokemon: list[str]

    def __init__(self):
        self.game = None
        self.progress = 0
        self.pokemon = [None, None, None, None, None, None]
