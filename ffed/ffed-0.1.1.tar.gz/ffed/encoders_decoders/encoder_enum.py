from enum import Enum

from ffed.encoders_decoders.encoders import (
    HTML,
    URL,
    AsciiDifferentBase,
    Base_x,
    DecimalDifferentBase,
)


class EncoderEnum(Enum):
    base16 = Base_x(16)
    base32 = Base_x(32)
    base64 = Base_x(64)
    base85 = Base_x(85)
    url = URL()
    html = HTML()
    ascii_bin = AsciiDifferentBase(2)
    ascii_oct = AsciiDifferentBase(8)
    ascii_hex = AsciiDifferentBase(16)
    binary = DecimalDifferentBase(2)
    octal = DecimalDifferentBase(8)
    hex = DecimalDifferentBase(16)
