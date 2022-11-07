from ffed import EncoderEnum

string_and_expected_output = {
    "url": {
        "string": 'http://example.org/"%<>\^`{|}',
        "expected_output": "http%3A%2F%2Fexample.org%2F%22%25%3C%3E%5C%5E%60%7B%7C%7D",
    },
    "html": {"string": "something", "expected_output": "something"},
    "binary": {"string": "1", "expected_output": "0b1"},
    "octal": {"string": "1", "expected_output": "0o1"},
    "hex": {"string": "1", "expected_output": "0x1"},
    "ascii_bin": {
        "string": 'hello world /"%<>\^`{|}',
        "expected_output": "0110100001100101011011000110110001101111001000000111011101101111011100100110110001100100001000000010111100100010001001010011110000111110010111000101111001100000011110110111110001111101",
    },
    "ascii_hex": {
        "string": 'hello world /"%<>\^`{|}',
        "expected_output": "68656c6c6f20776f726c64202f22253c3e5c5e607b7c7d",
    },
}


class TestEncoders:
    def test_encoders_all(self):
        for encoding_algo in string_and_expected_output.keys():
            encoding_algo_object = getattr(EncoderEnum, encoding_algo).value
            encoded_string = encoding_algo_object.encode(
                string_and_expected_output[encoding_algo]["string"]
            )

            assert (
                encoded_string
                == string_and_expected_output[encoding_algo]["expected_output"]
            )

            decoded_string = encoding_algo_object.decode(encoded_string)

            assert decoded_string == string_and_expected_output[encoding_algo]["string"]
