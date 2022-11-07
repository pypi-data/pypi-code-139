from enum import Enum

from ffed.hashes.hashes import LibraryHashes


class HashesEnum(Enum):
    md5 = LibraryHashes("md5")
    sha1 = LibraryHashes("sha1")
    sha224 = LibraryHashes("sha224")
    sha256 = LibraryHashes("sha256")
    sha384 = LibraryHashes("sha384")
    sha512 = LibraryHashes("sha512")
