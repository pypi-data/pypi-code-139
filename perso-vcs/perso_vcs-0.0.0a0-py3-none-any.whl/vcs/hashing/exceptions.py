from ..exceptions import PersoVCSBaseException


class HashException(PersoVCSBaseException):
    error_msg = "hash exception."


class InvalidHashFormatException(HashException):
    error_msg = "hash data format is invalid."


class HashAlgorithmNotSupportedException(HashException):
    error_msg = "hash algorithm {hash_algo} is not supported."
