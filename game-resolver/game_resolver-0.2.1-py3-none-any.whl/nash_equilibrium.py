from typing import Any, List

from game_resolver.actions import Actions
from game_resolver.games.game import Game
from game_resolver.util.cartesian_product import CartesianProduct


class NashEquilibrium:
    def __init__(self) -> None:
        pass

    def get_equilibrium(self, game: Game) -> List[Any]:
        equilibrium_list = []  # 均衡解のリスト

        actions_list: List[Actions] = []  # 各プレイヤの持つactions (リスト) のリスト
        for player in game.get_player_list():
            actions_list.append(player.get_actions())

        # ↓直積集合でループする
        c = CartesianProduct()
        for profile in c.product(*actions_list):  # type: ignore
            for player in game.get_player_list():
                if not player.check_best_response(profile):
                    break  # Best responseではないので、for文を抜ける

            # ↓playerのfor文が全部回ったので全員がBest response → 均衡
            else:
                equilibrium_list.append(profile)

        return equilibrium_list
