import itertools

from game_resolver.actions import Actions
from game_resolver.games.game import Game
from game_resolver.payoff import Payoff
from game_resolver.player import Player


class BattleOfSex(Game):
    def __init__(self) -> None:
        super().__init__()

        # 行動のインスタンス化
        actions = Actions(["Soccor", "Ballet"])

        # 利得の設定
        player1_payoff_list = [3, 0, 0, 1]
        player2_payoff_list = [1, 0, 0, 3]
        payoff1 = Payoff()
        counter = 0
        for i in itertools.product(actions, actions):
            payoff1.set(i, player1_payoff_list[counter])
            counter = counter + 1

        payoff2 = Payoff()
        counter = 0
        for i in itertools.product(actions, actions):
            payoff2.set(i, player2_payoff_list[counter])
            counter = counter + 1

        # プレイヤのインスタンス化
        player1 = Player(0, actions, payoff1)
        player2 = Player(1, actions, payoff2)
        self.add(player1)
        self.add(player2)
