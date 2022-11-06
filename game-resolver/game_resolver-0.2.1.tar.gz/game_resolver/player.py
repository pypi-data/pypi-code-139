from typing import Any, Tuple

from game_resolver.actions import Actions
from game_resolver.payoff import Payoff


class Player:
    def __init__(self, id: int, actions: Actions, payoff: Payoff) -> None:
        self._id = id
        self.__actions = actions
        self._payoff = payoff

    def get_actions(self) -> Actions:
        return self.__actions

    def get_payoff_value(self, strategy_profile: Tuple) -> float:
        value = self._payoff.get(strategy_profile)
        return value

    def check_best_response(self, strategy_profile: Tuple[Any]) -> bool:
        profile = list(strategy_profile)  # リストに変換
        utiliy_value = self.get_payoff_value(strategy_profile)

        for action in self.__actions:
            profile[self._id] = action
            temp = self.get_payoff_value(tuple(profile))
            if temp > utiliy_value:
                return False
        # ↓ for文が全部回ったらTrueを返す
        else:
            return True
