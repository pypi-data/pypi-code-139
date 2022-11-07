from ffed.encoders_decoders import EncoderEnum

expected_output = {"string": "foo bar", "base_64": "Zm9vIGJhcg=="}


class TestBaseX:
    def test_base_64(self):
        base64_object = EncoderEnum.base64.value
        test_string = expected_output["string"]
        encoded_string = base64_object.encode(test_string)

        assert encoded_string == expected_output["base_64"]

        decoded_string = base64_object.decode(encoded_string)

        assert decoded_string == test_string
