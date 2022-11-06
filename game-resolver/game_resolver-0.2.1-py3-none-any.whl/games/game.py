from typing import List

from game_resolver.player import Player


class Game:
    def __init__(self) -> None:
        self._player_list: List[Player] = []

    def add(self, player: Player) -> None:
        self._player_list.append(player)

    def get_player_list(self) -> List[Player]:
        return self._player_list
