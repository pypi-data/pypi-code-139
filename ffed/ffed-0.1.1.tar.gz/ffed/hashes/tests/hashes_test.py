from ffed import HashesEnum
from ffed.hashes.hashes import LibraryHashes

test_string = "Test String"
expected_output = {
    "md5": "bd08ba3c982eaad768602536fb8e1184",
    "sha1": "a5103f9c0b7d5ff69ddc38607c74e53d4ac120f2",
    "sha224": "a4342acc574edb5032b8b0f0fc0edeb5e4d977ca8c87a60214c62c69",
    "sha256": "30c6ff7a44f7035af933babaea771bf177fc38f06482ad06434cbcc04de7ac14",
    "sha384": "d76a1b44f76d7cfe3f1cc244078de956a23a0b34adea1321ce67b188929719750979db66f793abdf4f87481ceb1cf931",
    "sha512": "924bae629fbad5096a0a68929d5314d5b10b00108c5f9387c98d4c6cfe527a3cb6bba4303ed769c1feb38699800012b50c41e638bf0b47854f78344a3ac442a8",
}


class TestHashes:
    def test_hashes_all(self):
        for hash_algo in expected_output:
            hashing_algo_object: LibraryHashes = HashesEnum[hash_algo].value

            hashed_string = hashing_algo_object.generate_hexdigest(test_string)

            assert hashed_string == expected_output[hash_algo]
