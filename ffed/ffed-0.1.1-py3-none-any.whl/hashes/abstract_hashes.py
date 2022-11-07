from abc import ABC, abstractmethod


class AbstractHash(ABC):
    @abstractmethod
    def generate_hexdigest(self, plain_text: str):
        pass
