from game_resolver.actions import Actions
from game_resolver.games.game import Game
from game_resolver.payoff import Payoff
from game_resolver.player import Player


class Prisoner(Game):
    def __init__(self) -> None:
        super().__init__()

        # self.__player_list = []

        # 行動のインスタンス化
        actions = Actions(["Cooperate", "Defeat"])

        # 利得の設定
        payoff1 = Payoff()
        payoff1.set(("Cooperate", "Cooperate"), 3)
        payoff1.set(("Cooperate", "Defeat"), 0)
        payoff1.set(("Defeat", "Cooperate"), 5)
        payoff1.set(("Defeat", "Defeat"), 1)

        payoff2 = Payoff()
        payoff2.set(("Cooperate", "Cooperate"), 3)
        payoff2.set(("Cooperate", "Defeat"), 5)
        payoff2.set(("Defeat", "Cooperate"), 0)
        payoff2.set(("Defeat", "Defeat"), 1)

        # プレイヤのインスタンス化
        player1 = Player(0, actions, payoff1)
        player2 = Player(1, actions, payoff2)
        self.add(player1)
        self.add(player2)
