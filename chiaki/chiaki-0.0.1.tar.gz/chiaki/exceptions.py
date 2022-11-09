class ChiakiException(Exception):
    "Generic chiaki exception."
    pass


class ChiakiBadLangException(ChiakiException):
    "Specified language is not supported or does not exist."
    pass

