from typing import Any, Iterator, List


class Actions:
    def __init__(self, actions: List[Any]) -> None:
        self.actions = actions

    def __iter__(self) -> Iterator[Any]:
        return iter(self.actions)
