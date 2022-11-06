import itertools

import numpy as np

from game_resolver.actions import Actions
from game_resolver.games.game import Game
from game_resolver.payoff import Payoff
from game_resolver.player import Player


class CournotGame(Game):
    def __init__(self) -> None:
        super().__init__()

        # 行動のインスタンス化
        actions = Actions(np.arange(0, 101, 0.1).tolist())

        # 利得の設定
        payoff1 = Payoff()
        payoff2 = Payoff()
        for i, j in itertools.product(actions, actions):
            profit1 = (100 - i - j) * i - 40 * i
            profit2 = (100 - i - j) * j - 40 * j
            payoff1.set((i, j), profit1)
            payoff2.set((i, j), profit2)

        # プレイヤのインスタンス化
        player1 = Player(0, actions, payoff1)
        player2 = Player(1, actions, payoff2)
        self.add(player1)
        self.add(player2)
