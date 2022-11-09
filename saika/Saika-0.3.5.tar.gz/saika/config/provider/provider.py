from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from saika.config import BaseConfig


class ConfigProvider:
    def __init__(self):
        self._configs = []  # type: List[BaseConfig]
        self._data = {}

    def get(self, section) -> dict:
        return self._data.get(section)

    def attach(self, config):
        self._configs.append(config)

    def load(self):
        for config in self._configs:
            config.refresh()

    def save(self):
        pass

    @property
    def data(self):
        return {config.section: config.data for config in self._configs}
