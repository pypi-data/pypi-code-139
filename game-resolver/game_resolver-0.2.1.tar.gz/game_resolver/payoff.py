from typing import Dict, Tuple


class Payoff:
    def __init__(self) -> None:
        self._profile_payoff_dict: Dict[Tuple, float] = {}  # 初期化

    def set(
        self,
        strategy_profile: Tuple,
        payoff_value: float,
    ) -> None:
        self._profile_payoff_dict[strategy_profile] = payoff_value

    def get(
        self,
        strategy_profile: Tuple,
    ) -> float:
        """
        利得関数の値を返す。
        """
        return self._profile_payoff_dict[strategy_profile]
