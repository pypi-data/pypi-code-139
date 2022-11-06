from typing import List, Tuple

from game_resolver.actions import Actions
from game_resolver.games.game import Game
from game_resolver.payoff import Payoff
from game_resolver.player import Player


class CustomGame(Game):
    def __init__(
        self,
        name: str,
        player_num: int,
        action_list: List[str],
        all_player_action_list: List[Tuple[str]],
        payoff_list: List[List[int]],
    ) -> None:
        super().__init__()

        self.name = name

        actions = Actions(action_list)

        for idx in range(len(payoff_list)):
            assert (
                len(payoff_list[idx]) == len(action_list) ** player_num
            ), f"payoff_list {idx} length mismatch with player_num, action_list"

        for player_idx, _payoff_list in enumerate(payoff_list):
            _payoff = Payoff()
            for idx, action in enumerate(all_player_action_list):
                _payoff.set(action, _payoff_list[idx])

            player = Player(player_idx, actions, _payoff)
            self.add(player)
