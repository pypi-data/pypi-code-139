from abc import ABC, abstractmethod


class AbstractEncoderDecoder(ABC):
    @abstractmethod
    def encode(self, plain_text: str):
        pass

    @abstractmethod
    def decode(self, encoded_string: str):
        pass
