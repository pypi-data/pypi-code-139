import hashlib
import pathlib
import re
import typing

import _hashlib

from ..settings import get_settings
from .exceptions import HashAlgorithmNotSupportedException, InvalidHashFormatException

_hash_format: str = "{hash_algo}@{hash}"

_hash_format_regex: re.Pattern = re.compile(r"^([a-z0-9]+)@([0-9a-f]+)$")


def get_hasher(hash_algo: str = get_settings().allowed_hashes[0]) -> _hashlib.HASH:
    if hash_algo not in get_settings().allowed_hashes:
        raise HashAlgorithmNotSupportedException(hash_algo=hash_algo)
    return hashlib.new(hash_algo)


def write_hash(hasher: _hashlib.HASH) -> str:
    hash_algo = hasher.name
    hash = hasher.hexdigest()
    return _hash_format.format(hash_algo=hash_algo, hash=hash)


def verify_hash(hash: str) -> typing.Tuple[str, str, str]:
    match = re.match(_hash_format_regex, hash)
    if not match:
        raise InvalidHashFormatException()

    hash_algo, hash_value = match.groups()
    if hash_algo not in get_settings().allowed_hashes:
        raise HashAlgorithmNotSupportedException(hash_algo=hash_algo)

    if get_hasher(hash_algo).digest_size * 2 != len(hash_value):
        raise InvalidHashFormatException()
    return hash, hash_algo, hash_value


def compute_hash_file(
    file: pathlib.Path, hash_algo: str = get_settings().allowed_hashes[0]
) -> str:
    if not file.exists():
        raise OSError(f"{file} does not exist.")
    if not file.is_file():
        raise OSError(f"{file} is not a file.")
    hasher = get_hasher(hash_algo)

    with file.open("rb") as f:
        for chunk in iter(lambda: f.read(get_settings().chunk_size), b""):
            hasher.update(chunk)
    hash_value = write_hash(hasher)

    return hash_value
