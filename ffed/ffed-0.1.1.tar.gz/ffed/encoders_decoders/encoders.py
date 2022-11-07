import base64
import html
from dataclasses import dataclass
from math import log
from urllib import parse

from ffed.custom_exceptions import EncoderException
from ffed.encoders_decoders.abstract_encoder_decoder import AbstractEncoderDecoder


@dataclass
class Base_x(AbstractEncoderDecoder):
    base: str

    def encode(self, plain_text: str):
        encoder = getattr(base64, f"b{self.base}encode")

        return encoder(plain_text.encode()).decode()

    def decode(self, encoded_string: str):
        decoder = getattr(base64, f"b{self.base}decode")

        return decoder(encoded_string.encode()).decode()


class URL(AbstractEncoderDecoder):
    def encode(self, plain_test: str):
        return parse.quote(plain_test, safe="")

    def decode(self, encoded_string: str):
        return parse.unquote(encoded_string)


class HTML(AbstractEncoderDecoder):
    def encode(self, plain_text: str):
        return html.escape(plain_text)

    def decode(self, encoded_string: str):
        return html.unescape(encoded_string)


@dataclass
class AsciiDifferentBase(AbstractEncoderDecoder):
    base: int
    __base_function = {2: bin, 16: hex}
    __length_multiple = {2: 8, 16: 2}

    def encode(self, plain_text: str):
        integer_from_bytes = int.from_bytes(plain_text.encode(), "big")
        base_converted_string = self.__base_function[self.base](integer_from_bytes)[2:]

        length_multiple = self.__length_multiple[self.base]
        num_of_zeroes_to_prepend = (
            length_multiple - (len(base_converted_string) % length_multiple)
        ) % length_multiple

        zeroes_appended_base_converted_string = base_converted_string.zfill(
            len(base_converted_string) + num_of_zeroes_to_prepend
        )

        return zeroes_appended_base_converted_string

    def decode(self, string: str):
        string = string.replace(" ", "")
        try:
            integer = int(string, self.base)
        except ValueError:
            raise EncoderException(
                f"provided value {string} is not a {self.base} number"
            )

        byte_string = integer.to_bytes(
            int(len(string) / (8 / log(self.base, 2))), "big"
        )

        return byte_string.decode()


@dataclass
class DecimalDifferentBase(AbstractEncoderDecoder):
    base: int
    base_function = {2: bin, 8: oct, 16: hex}

    def encode(self, int_string: str):
        try:
            integer = int(int_string)

        except ValueError:
            raise EncoderException(f"provided value {int_string} is not an integer")

        return self.base_function[self.base](integer)

    def decode(self, string: str):
        try:
            integer = int(string, self.base)

        except ValueError:
            raise EncoderException(
                f"provided value {string} is not a base{self.base} number"
            )

        return str(integer)
