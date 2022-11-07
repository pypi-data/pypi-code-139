import os
import sys

from ffed import EncoderEnum, HashesEnum
from ffed.custom_exceptions import InputException
from ffed.encoders_decoders.abstract_encoder_decoder import AbstractEncoderDecoder
from ffed.hashes.abstract_hashes import AbstractHash


class FFED_Adapter:
    def __stdin(self, dummy_variable):
        if not os.isatty(sys.stdin.fileno()):
            raise InputException("stdin option selected but no input given")

        stdin_content_generator = (line for line in sys.stdin)

        text = "".join(stdin_content_generator)

        return text

    def __file(self, file_name):

        with open(file_name, "r") as file:
            file_content_generator = (line for line in file)

            text = "".join(file_content_generator)

            return text

    def __string(self, string):
        return string

    def __get_input(self, input_options: dict):
        input_option = list(input_options)[0]
        text = getattr(self, f"_FFED_Adapter__{input_option}")(
            input_options[input_option]
        )
        return text

    def __output(self, text, output_file: str):

        if not output_file:
            return text

        with open(output_file, "w") as file:
            file.write(text)

    def encode(self, verbose: int, algos: tuple, out: str, **input_options):
        plain_text = self.__get_input(input_options)

        encoded_string = plain_text
        for algo in algos:
            encoding_algo: AbstractEncoderDecoder = EncoderEnum[algo].value
            encoded_string = encoding_algo.encode(encoded_string)

        return self.__output(encoded_string, out)

    def decode(self, verbose: int, algos: tuple, out: str, **input_options):
        encoded_text = self.__get_input(input_options)

        decoded_string = encoded_text

        for algo in algos:
            decoding_algo: AbstractEncoderDecoder = EncoderEnum[algo].value
            decoded_string = decoding_algo.decode(decoded_string)

        return self.__output(decoded_string, out)

    def hash(self, verbose: int, algos: tuple, out: str, **input_options):
        plain_text = self.__get_input(input_options)

        hashed_text = plain_text

        for algo in algos:
            hashing_algo: AbstractHash = HashesEnum[algo].value
            hashed_text = hashing_algo.generate_hexdigest(hashed_text)

        return self.__output(hashed_text, out)
