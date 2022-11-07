from dataclasses import dataclass
from hashlib import new

from ffed.hashes.abstract_hashes import AbstractHash


@dataclass()
class LibraryHashes(AbstractHash):
    algo: str

    def generate_hexdigest(self, input_string: str):
        return new(self.algo, input_string.encode()).hexdigest()
